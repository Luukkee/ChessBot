import os
model_folder_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'model'))
try:
    from .engineModel import *
except ImportError:
    from engineModel import *
    model_file_path = os.path.join(model_folder_path, 'savedModels/updated_again_model_current.pth')

    model = ChessNet()
    model.load_state_dict(torch.load(model_file_path))
    model.eval()
import chess
import chess.pgn
import random
import numpy as np
#from model import eco, ChessNet



def load_openings_from_pgn(pgn_file):
    openings = []
    with open(pgn_file) as f:
        while True:
            game = chess.pgn.read_game(f)
            if game is None:
                break

            board = game.board()
            moves = []
            for move in game.mainline_moves():
                moves.append(board.san(move))
                board.push(move)

            openings.append(moves)
    return openings

#Function to find matching openings based on played moves
def find_matching_openings(played_moves, openings):
    """
    Finding opening works by checking if the played moves match the start of any opening in the opening book.
    This is because a chosen opening can be diverged from at any point by the opponent.
    This makes the bot more dynamic in the opening phase.
    """
    matching_openings = []
    for opening in openings:
        if played_moves == opening[:len(played_moves)]:
            matching_openings.append(opening)
    return matching_openings

#Function to choose the next move from matching openings
def select_next_move(played_moves, matching_openings, rand = True):
    if not matching_openings:
        return None  # No matching opening found, time for engine

    if rand:
        chosen_opening = random.choice(matching_openings)

        if len(chosen_opening) > len(played_moves):
            next_move = chosen_opening[len(played_moves)]
            return next_move
    else:
        for opening in matching_openings:
            if len(opening) > len(played_moves):
                next_move = opening[len(played_moves)]
                return next_move
    return None  # No more moves in the opening book, time for engine

def board_to_input(board, is_white):
    board_planes = torch.zeros((8, 8, 13), dtype=torch.float32)

    # Iterate over the board's rows and columns (flipped, so row 0 is black's side) 
    # because the developer was naive enough to believe it would not matter 
    # and lazy enough to find temporary solutions to the problem along the way
    for row in range(8):
        for col in range(8):
            piece = board.piece_at(row, col)  # Get the piece at the current (row, col)
            if piece:
                # Determine the plane based on the piece id and color
                plane = piece.id - 1  # piece.id ranges from 1 to 6 (pawn, knight, etc.)
                if piece.color == 'black':
                    plane += 6  # Shift to black piece planes (6-11)

                # Invert the row index since row 0 on my board is actually row 7 in the neural net input
                inverted_row = 7 - row

                # Place the piece on the correct plane in the board_planes array
                board_planes[inverted_row, col, plane] = 1

    # Set the last plane to indicate which side the engine is playing (1 for white, 0 for black)
    board_planes[:, :, 12] = 1.0 if is_white else 0.0
    board_input = board_planes.unsqueeze(0).permute(0, 3, 1, 2) 

    return board_input



def predict_move(model, board):
    board_input = board_to_input(board, board.current_turn == 'white')
    with torch.no_grad():
        output = model(board_input)
    
    move_scores = output.squeeze().sort(descending=True)
    move_indices = move_scores.indices.tolist()
    
    for move_index in move_indices:
        from_square = move_index // 64
        print(from_square)
        to_square = move_index % 64
        move = chess.Move(from_square, to_square)
        # If pawn and last character is 1 or eight, add 'q' to the move
        # Hopefully this works, always promotes to queen
        # Might be redundant right now
        tmp_board = chess.Board(board.generate_fen())

        if tmp_board.piece_at(from_square).piece_type == 1 and (str(move)[-1] == '1' or str(move)[-1] == '8'):
            move = chess.Move(from_square, to_square, promotion=5)  
        print(move, move_scores.values[move_index].item())
        
        

        if move in tmp_board.legal_moves:
            del tmp_board
            return move
    
    # If no valid moves are found (which shouldn't happen), return None
    return None

openings_file_path = os.path.join(model_folder_path, "eco.pgn")
openings = load_openings_from_pgn(openings_file_path)

class Engine:
    def __init__(self, color="white", opening_phase=True, played_moves=[]):
        self.played_moves = played_moves
        self.opening_phase = opening_phase
        self.color = color

    def square_to_algebraic(self, row, col):
        """
        Convert (row, col) to algebraic notation (e.g., (6, 3) -> 'd2').
        Inverts the row to match algebraic notation.
        """
        files = 'abcdefgh'
        rank = 8 - row  # Invert row for algebraic rank (1-8)
        file = files[col]  # Get file from 'a'-'h'
        return f"{file}{rank}"

    def update(self, move, board, actual = True):
        from_square, to_square = move
        from_row, from_col = from_square
        to_row, to_col = to_square

        from_square_algebraic = self.square_to_algebraic(from_row, from_col)
        to_square_algebraic = self.square_to_algebraic(to_row, to_col)

        # Combine both into uci format (e.g., 'd2d4')
        uci_move = f"{from_square_algebraic}{to_square_algebraic}"
        move_obj = chess.Move.from_uci(uci_move)

        fen = board.generate_fen()
        tmp_board = chess.Board(fen)
        move = tmp_board.san(move_obj)

        del tmp_board
        if actual:
            self.played_moves.append(move)
        return move

    def engine_move(self, board, model = None):
        if self.opening_phase:
            matching_openings = find_matching_openings(self.played_moves, openings)
            next_move = select_next_move(self.played_moves, matching_openings)
        if self.opening_phase and next_move:
            print("Opening move")
            self.played_moves.append(next_move)
            fen = board.generate_fen()
            tmp_board = chess.Board(fen)
            move = tmp_board.parse_san(next_move)
            # Really ugly, but I made my own parse_move in the board class. 
            # Does not look pretty right below the Chess library's parse_san, 
            # but theirs simplify the notation while mine converts it to the notation my board uses.
            move_a = board.parse_move(move) 
            del tmp_board
            return move_a, move
        else:
            print("Engine move")
            print(board.current_turn)
            if (board.current_turn == self.color):
                bot_move = predict_move(model, board)
                print(bot_move)
                self.opening_phase = False
                if bot_move:
                    return board.parse_move(bot_move), bot_move
                else:
                    return None
            else:
                return None