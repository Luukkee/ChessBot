""""""""""""""""""
"  CHESS  LOGIC  "
""""""""""""""""""
SQUARES = [(x, y) for x in range(8) for y in range(8)]


class Piece:
    def __init__(self, color):
        self.color = color

    def fen_char(self):
        pass

    def get_moves(self, board, row, col, not_safe):
        pass

class King(Piece):
    def __init__(self, color):
        super().__init__(color)
        self.piece_type = 'king'
        self.id = 6

    def fen_char(self):
        return 'K' if self.color == 'white' else 'k'

    def get_moves(self, board, row, col, not_safe = False):
        moves = []
        for i in range(-1, 2):
            for j in range(-1, 2):
                if i == 0 and j == 0:
                    continue
                new_row, new_col = row + i, col + j
                if 0 <= new_row < 8 and 0 <= new_col < 8:
                    piece = board.piece_at(new_row, new_col)
                    if (not piece or piece.color != self.color) and (not_safe or board.is_safe_move(self, (row, col), (new_row, new_col))):
                        moves.append((new_row, new_col))
        
        if board.castling_rights[self.color]['kingside']:
            if not board.piece_at(row, 5) and not board.piece_at(row, 6):
                rook = board.piece_at(row, 7)
                if rook and rook.piece_type == 'rook' and rook.color == self.color:
                    if (not_safe or not board.is_in_check(self.color) and 
                        not board.is_under_attack(row, 4, self.color) and 
                        not board.is_under_attack(row, 5, self.color) and 
                        not board.is_under_attack(row, 6, self.color)):
                        if (not_safe or board.is_safe_move(self, (row, col), (row, 6))):  
                            moves.append((row, 6))
        if board.castling_rights[self.color]['queenside']:
            if not board.piece_at(row, 1) and not board.piece_at(row, 2) and not board.piece_at(row, 3):
                rook = board.piece_at(row, 0)
                if rook and rook.piece_type == 'rook' and rook.color == self.color:
                    if (not_safe or not board.is_in_check(self.color) and 
                        not board.is_under_attack(row, 4, self.color) and 
                        not board.is_under_attack(row, 3, self.color) and 
                        not board.is_under_attack(row, 2, self.color)):
                        if (not_safe or board.is_safe_move(self, (row, col), (row, 2))):  
                            moves.append((row, 2))
        return moves

class Queen(Piece):
    def __init__(self, color):
        super().__init__(color)
        self.piece_type = 'queen'
        self.id = 5
    
    def fen_char(self):
        return 'Q' if self.color == 'white' else 'q'

    def get_moves(self, board, row, col, not_safe = False):
        moves = []
        for i in range(-1, 2):
            for j in range(-1, 2):
                if i == 0 and j == 0:
                    continue
                new_row, new_col = row + i, col + j
                while 0 <= new_row < 8 and 0 <= new_col < 8:
                    piece = board.piece_at(new_row, new_col)
                    if (not piece or piece.color != self.color):
                        if (not_safe or board.is_safe_move(self, (row, col), (new_row, new_col))):
                            moves.append((new_row, new_col))
                            if piece:
                                break
                    else:
                        break
                    new_row += i
                    new_col += j
        return moves

class Rook(Piece):
    def __init__(self, color):
        super().__init__(color)
        self.piece_type = 'rook'
        self.id = 4

    def fen_char(self):
        return 'R' if self.color == 'white' else 'r'

    def get_moves(self, board, row, col, not_safe = False):
        moves = []
        for i in range(-1, 2, 2):
            new_row, new_col = row + i, col
            while 0 <= new_row < 8:
                piece = board.piece_at(new_row, new_col)
                if (not piece or piece.color != self.color):
                    if (not_safe or board.is_safe_move(self, (row, col), (new_row, new_col))):
                        moves.append((new_row, new_col))
                        if piece:
                            break
                elif (piece or piece.color == self.color):
                    break
                new_row += i
        for i in range(-1, 2, 2):
            new_row, new_col = row, col + i
            while 0 <= new_col < 8:
                piece = board.piece_at(new_row, new_col)
                if (not piece or piece.color != self.color):
                    if (not_safe or board.is_safe_move(self, (row, col), (new_row, new_col))):
                        moves.append((new_row, new_col))
                        if piece:
                            break
                else:
                    break
                new_col += i
        return moves

class Bishop(Piece):
    def __init__(self, color):
        super().__init__(color)
        self.piece_type = 'bishop'
        self.id = 3

    def fen_char(self):
        return 'B' if self.color == 'white' else 'b'

    def get_moves(self, board, row, col, not_safe = False):
        moves = []
        for i in range(-1, 2, 2):
            for j in range(-1, 2, 2):
                new_row, new_col = row + i, col + j
                while 0 <= new_row < 8 and 0 <= new_col < 8:
                    piece = board.piece_at(new_row, new_col)
                    if (not piece or piece.color != self.color):
                        if (not_safe or board.is_safe_move(self, (row, col), (new_row, new_col))):
                            moves.append((new_row, new_col))
                            if piece:
                                break
                    else:
                        break
                    new_row += i
                    new_col += j
        return moves

class Knight(Piece):
    def __init__(self, color):
        super().__init__(color)
        self.piece_type = 'knight'
        self.id = 2

    def fen_char(self):
        return 'N' if self.color == 'white' else 'n'

    def get_moves(self, board, row, col, not_safe = False):
        moves = []
        for i in [-2, -1, 1, 2]:
            for j in [-2, -1, 1, 2]:
                if abs(i) != abs(j):
                    new_row, new_col = row + i, col + j
                    if 0 <= new_row < 8 and 0 <= new_col < 8:
                        piece = board.piece_at(new_row, new_col)
                        if (not piece or piece.color != self.color) and (not_safe or board.is_safe_move(self, (row, col), (new_row, new_col))):
                            moves.append((new_row, new_col))
        return moves

class Pawn(Piece):
    def __init__(self, color):
        super().__init__(color)
        self.piece_type = 'pawn'
        self.id = 1

    def fen_char(self):
        return 'P' if self.color == 'white' else 'p'

    def get_moves(self, board, row, col, not_safe = False):
        moves = []
        direction = -1 if self.color == 'white' else 1
        new_row, new_col = row + direction, col
        # Single-square advance
        new_row, new_col = row + direction, col
        if 0 <= new_row < 8:
            piece = board.piece_at(new_row, new_col)
            if (not piece) and (not_safe or board.is_safe_move(self, (row, col), (new_row, new_col))):
                moves.append((new_row, new_col))

        # Double-square advance (only from the starting row) - consider independently of the first step
        if (row == 1 and self.color == 'black') or (row == 6 and self.color == 'white'):
            new_row = row + 2 * direction
            new_col = col
            if 0 <= new_row < 8:  # Ensure the move is within bounds
                piece = board.piece_at(new_row, new_col)
                # Ensure the square is empty and check if the double move is valid independently
                if (not piece) and board.piece_at(row + direction, col) is None:  # Ensure the intermediate square is empty
                    if (not_safe or board.is_safe_move(self, (row, col), (new_row, new_col))):
                        moves.append((new_row, new_col))
        for i in [-1, 1]:
            #en passant
            if (board.en_passant_target and board.en_passant_target == (row + direction, col + i)) and (not_safe or board.is_safe_move(self, (row, col), (row + direction, col + i), True)):
                moves.append((row + direction, col + i))
            new_row, new_col = row + direction, col + i
            if 0 <= new_row < 8 and 0 <= new_col < 8:
                piece = board.piece_at(new_row, new_col)
                if (piece and piece.color != self.color) and (not_safe or board.is_safe_move(self, (row, col), (new_row, new_col))):
                    moves.append((new_row, new_col))
        return moves

class Board:
    def __init__(self, fen=None):
        self.board = self.create_board()
        self.current_turn = 'white'
        self.en_passant_target = None
        self.promotion = None
        self.castling_rights = {'white': {'kingside': True, 'queenside': True},
                                'black': {'kingside': True, 'queenside': True}}
        
        if fen:
            self.load_fen(fen)
        else:
            self.board = self.create_board()
    
    # Parse fen string to board state
    def load_fen(self, fen):
        parts = fen.split()
        piece_placement = parts[0]
        self.current_turn = 'white' if parts[1] == 'w' else 'black'
        self.castling_rights = self.parse_castling_rights(parts[2])
        self.en_passant_target = self.parse_en_passant(parts[3]) if parts[3] != '-' else None
        
        # Clear the board and place the pieces from the FEN string
        self.board = [[None for _ in range(8)] for _ in range(8)] 
        ranks = piece_placement.split('/')
        for rank_idx, rank in enumerate(ranks):
            file_idx = 0
            for char in rank:
                if char.isdigit():
                    file_idx += int(char)  # Skip empty squares
                else:
                    color = 'white' if char.isupper() else 'black'
                    piece_type = char.lower()
                    piece = self.create_piece(piece_type, color)
                    self.board[rank_idx][file_idx] = piece
                    file_idx += 1

    def parse_castling_rights(self, castling_str):
        """
        Parses the castling rights from the FEN string and returns a dictionary.
        Example input: 'KQkq'
        Example output: {'white': {'kingside': True, 'queenside': True}, 'black': {'kingside': True, 'queenside': True}}
        """
        castling_rights = {'white': {'kingside': False, 'queenside': False},
                            'black': {'kingside': False, 'queenside': False}}
        if 'K' in castling_str:
            castling_rights['white']['kingside'] = True
        if 'Q' in castling_str:
            castling_rights['white']['queenside'] = True
        if 'k' in castling_str:
            castling_rights['black']['kingside'] = True
        if 'q' in castling_str:
            castling_rights['black']['queenside'] = True

        return castling_rights
    
    def parse_en_passant(self, en_passant_str):
        """
        Parses the en passant target square from the FEN string.
        Converts algebraic notation (e.g., 'e3') to (row, col) tuple.
        Returns None if no en passant is possible.
        """
        if en_passant_str == '-':
            return None  # No en passant target

        files = 'abcdefgh'
        file = en_passant_str[0]  # Column letter (e.g., 'e')
        rank = en_passant_str[1]  # Row number (e.g., '3')

        col = files.index(file)  # Convert file ('a'-'h') to column index (0-7)
        row = 8 - int(rank)      # Convert rank ('1'-'8') to row index (7-0)

        return (row, col)

    # Helper to create pieces from the FEN character
    def create_piece(self, piece_type, color):
        if piece_type == 'p':
            return Pawn(color)
        elif piece_type == 'r':
            return Rook(color)
        elif piece_type == 'n':
            return Knight(color)
        elif piece_type == 'b':
            return Bishop(color)
        elif piece_type == 'q':
            return Queen(color)
        elif piece_type == 'k':
            return King(color)
        
    def get_castling_rights_fen(self):
        rights = []
        if self.castling_rights['white']['kingside']:
            rights.append('K')
        if self.castling_rights['white']['queenside']:
            rights.append('Q')
        if self.castling_rights['black']['kingside']:
            rights.append('k')
        if self.castling_rights['black']['queenside']:
            rights.append('q')
        return ''.join(rights) or '-'

    # Helper to get FEN for en passant target
    def get_en_passant_fen(self):
        if self.en_passant_target:
            files = 'abcdefgh'
            row, col = self.en_passant_target
            return f"{files[col]}{8 - row}"
        return '-'  # No en passant target

    # Generate FEN string from the current board state
    def generate_fen(self):
        fen = []
        for row in self.board:
            empty_squares = 0
            fen_row = ''
            for piece in row:
                if piece is None:
                    empty_squares += 1
                else:
                    if empty_squares > 0:
                        fen_row += str(empty_squares)
                        empty_squares = 0
                    fen_row += piece.fen_char()
            if empty_squares > 0:
                fen_row += str(empty_squares)
            fen.append(fen_row)
        piece_placement = '/'.join(fen)

        turn = 'w' if self.current_turn == 'white' else 'b'
        castling = self.get_castling_rights_fen()
        en_passant = self.get_en_passant_fen()
        halfmove_clock = '0'  
        fullmove_number = '1' # Not caring enough to implement this

        return f"{piece_placement} {turn} {castling} {en_passant} {halfmove_clock} {fullmove_number}"

    def algebraic_to_index(self, square):
        """
        Convert from algebraic notation (e.g., 'd2') to (row, col).
        'a'-'h' -> 0-7 and '1'-'8'.
        """
        files = 'abcdefgh'  # Columns 'a'-'h'
        col = files.index(square[0])  # Get column index from 'a'-'h'
        row = int(square[1]) - 1  # Get row index 
        return (row, col)  # Does not invert board here because it gets inverted later

    def square_to_algebraic(self, row, col):
        """
        Convert (row, col) to algebraic notation (e.g., (6,3) -> 'd2').
        Inverts the row to match algebraic notation.
        """
        files = 'abcdefgh'
        rank = 8 - row  # Invert row for algebraic rank (1-8)
        file = files[col]  # Get file from 'a'-'h'
        return f"{file}{rank}"

    def square_index_to_row_col(self, square_index):
        """
        Convert square index (0-63) to (row, col).
        Square index 0 starts at 'a8', square index 63 is 'h1'.
        """
        row = square_index // 8  # Integer division to get row
        col = square_index % 8   # Modulo to get column
        return (row, col)

    def parse_move(self, move):
        """
        Parse a Move class instance to from_square and to_square.
        """
        # Convert the move from the Move class to algebraic notation

        from_row_col = self.square_index_to_row_col(move.from_square)
        to_row_col = self.square_index_to_row_col(move.to_square)

        # Convert row, col to algebraic notation
        from_square = self.square_to_algebraic(*from_row_col)
        to_square = self.square_to_algebraic(*to_row_col)

        # Convert algebraic squares to (row, col)
        from_pos = self.algebraic_to_index(from_square)
        to_pos = self.algebraic_to_index(to_square)

        return from_pos, to_pos

    def create_board(self):
        """
        Create a new chess board with pieces in starting positions.
        Only called if no FEN string is provided.
        """
        # Create an 8x8 board with pieces placed in starting positions
        board = [[None for _ in range(8)] for _ in range(8)]
        # Place pieces on the board 
        board[0][0] = Rook('black')
        board[0][7] = Rook('black')
        board[7][7] = Rook('white')
        board[7][0] = Rook('white')
        board[0][1] = Knight('black')
        board[0][6] = Knight('black')
        board[7][1] = Knight('white')
        board[7][6] = Knight('white')
        board[0][2] = Bishop('black')
        board[0][5] = Bishop('black')
        board[7][2] = Bishop('white')
        board[7][5] = Bishop('white')
        board[0][3] = Queen('black')
        board[7][3] = Queen('white')
        board[0][4] = King('black')
        board[7][4] = King('white')
        for i in range(8):
            board[1][i] = Pawn('black')
            board[6][i] = Pawn('white')

        return board
    
    def piece_at(self, row, col):
        return self.board[row][col]

    def move_piece(self, start_pos, end_pos, engine=None):
        piece = self.piece_at(*start_pos)

        if piece and piece.color == self.current_turn:
            if end_pos in piece.get_moves(self, *start_pos):
                if engine:
                    move = (start_pos, end_pos)
                    engine.update(move, self)
                self.handle_special_moves(piece, start_pos, end_pos)
                self.board[end_pos[0]][end_pos[1]] = piece
                self.board[start_pos[0]][start_pos[1]] = None
                self.current_turn = 'black' if self.current_turn == 'white' else 'white'

                if self.is_in_check(self.current_turn):
                    print(f"Check! {self.current_turn} is in check.")
                    
                    # Check for checkmate
                    if self.is_checkmate(self.current_turn):
                        print(f"Checkmate! {self.current_turn} loses the game.")
                        return True  # Game over
                elif self.is_stalemate(self.current_turn):
                    print("Stalemate! The game is a draw.")
                    return True

                return True
        return False

    def is_valid_move(self, start_pos, end_pos):
        # TODO: Implement functionality for forced moves (eg. checks)
        piece = self.piece_at(*start_pos)
        if piece and piece.color == self.current_turn:
            return end_pos in piece.get_moves(self, *start_pos)
        return False
    
    def promotion_piece(self, piece):
        if self.promotion:
            if piece == 'queen':
                piece = Queen(self.piece_at(*self.promotion).color)
            elif piece == 'rook':
                piece = Rook(self.piece_at(*self.promotion).color)
            elif piece == 'bishop':
                piece = Bishop(self.piece_at(*self.promotion).color)
            elif piece == 'knight':
                piece = Knight(self.piece_at(*self.promotion).color)
            self.board[self.promotion[0]][self.promotion[1]] = piece
            self.promotion = None

    def handle_special_moves(self, piece, start_pos, end_pos):
        #print(end_pos)
        # takes with en passant
        if piece.piece_type == 'pawn' and end_pos == self.en_passant_target:
            self.board[start_pos[0]][end_pos[1]] = None
        # Handle en passant
        if piece.piece_type == 'pawn' and abs(start_pos[0] - end_pos[0]) == 2:
            self.en_passant_target = ((start_pos[0] + end_pos[0]) // 2, start_pos[1])
        else:
            self.en_passant_target = None
        # Promotion
        if piece.piece_type == 'pawn' and (end_pos[0] == 0 or end_pos[0] == 7):
            self.promotion = end_pos
        # Handle castling
        if piece.piece_type == 'king' and abs(start_pos[1] - end_pos[1]) == 2:
            if end_pos[1] == 6:
                self.board[end_pos[0]][5] = self.board[end_pos[0]][7]
                self.board[end_pos[0]][7] = None
            elif end_pos[1] == 2:
                self.board[end_pos[0]][3] = self.board[end_pos[0]][0]
                self.board[end_pos[0]][0] = None
        # Update castling rights
        if piece.piece_type == 'rook' and start_pos[1] == 0:
            self.castling_rights[piece.color]['queenside'] = False
        elif piece.piece_type == 'rook' and start_pos[1] == 7:
            self.castling_rights[piece.color]['kingside'] = False
        elif piece.piece_type == 'king':
            self.castling_rights[piece.color]['kingside'] = False
            self.castling_rights[piece.color]['queenside'] = False


    # Handle check
    def is_under_attack(self, row, col, color):
        # TODO: Re-check thisfunction
        opponent_color = 'black' if color == 'white' else 'white'
        for r in range(8):
            for c in range(8):
                piece = self.piece_at(r, c)
                if piece and piece.color == opponent_color:
                    if (row, col) in piece.get_moves(self, r, c, True):
                        return True
        return False

    def find_king(self, color):
        for r in range(8):
            for c in range(8):
                piece = self.piece_at(r, c)
                if piece and piece.piece_type == 'king' and piece.color == color:
                    return (r, c)
        return None

    def is_in_check(self, color):
        king_pos = self.find_king(color)
        if king_pos:
            return self.is_under_attack(*king_pos, color)
        return False
    
    def is_checkmate(self, color):
        """
        Checks if the player of the given color is in checkmate.
        """
        # If the player is not in check, it's not checkmate
        if not self.is_in_check(color):
            return False

        # Check all pieces of the current player
        for row in range(8):
            for col in range(8):
                piece = self.piece_at(row, col)
                if piece and piece.color == color:
                    # Get all possible moves for the piece
                    possible_moves = piece.get_moves(self, row, col, True)
                    for move in possible_moves:
                        # Make a hypothetical move and check if it resolves the check
                        original_piece = self.piece_at(*move)
                        self.board[move[0]][move[1]] = piece
                        self.board[row][col] = None

                        if not self.is_in_check(color):
                            # Undo the move
                            self.board[row][col] = piece
                            self.board[move[0]][move[1]] = original_piece
                            return False  # There's at least one valid move, so no checkmate

                        # Undo the move
                        self.board[row][col] = piece
                        self.board[move[0]][move[1]] = original_piece

        # No valid moves found, it's checkmate
        return True
    
    def is_stalemate(self, color):
        """
        Checks if the current player of the given color is in stalemate.
        Stalemate occurs if the player is not in check but has no legal moves.
        """
        # Step 1: The player must not be in check
        if self.is_in_check(color):
            return False

        # Step 2: Check if the player has any legal moves
        for row in range(8):
            for col in range(8):
                piece = self.piece_at(row, col)
                if piece and piece.color == color:
                    possible_moves = piece.get_moves(self, row, col, True)
                    for move in possible_moves:
                        # Simulate the move to see if it leaves the King in check
                        original_piece = self.piece_at(*move)
                        self.board[move[0]][move[1]] = piece
                        self.board[row][col] = None

                        if not self.is_in_check(color):
                            # Undo the move
                            self.board[row][col] = piece
                            self.board[move[0]][move[1]] = original_piece
                            return False  # The player has at least one valid move

                        # Undo the move
                        self.board[row][col] = piece
                        self.board[move[0]][move[1]] = original_piece

        # If no valid moves are found and the player is not in check, it's stalemate
        return True
        
    def is_safe_move(self, piece, start_pos, end_pos, en_passant=False):
        """
        Simulates a move and checks if it leaves the player's king in check.
        """
        original_piece = self.piece_at(*end_pos)
        self.board[end_pos[0]][end_pos[1]] = piece  # Make the move
        self.board[start_pos[0]][start_pos[1]] = None
        tmp_piece = None  # Track en passant captures

        # Handle en passant captures
        if en_passant and self.en_passant_target:
            tmp_piece = self.piece_at(start_pos[0], end_pos[1])
            self.board[start_pos[0]][end_pos[1]] = None

        is_safe = not self.is_in_check(piece.color)  # Check if king is safe
        

        # Undo the move
        self.board[start_pos[0]][start_pos[1]] = piece
        self.board[end_pos[0]][end_pos[1]] = original_piece

        if en_passant and self.en_passant_target:
            print(self.en_passant_target)
            print("EN PASSANT")
            print(start_pos[0], end_pos[1])
            print(tmp_piece)
            print(is_safe)
            print(self.generate_fen())
            self.board[start_pos[0]][end_pos[1]] = tmp_piece

        return is_safe