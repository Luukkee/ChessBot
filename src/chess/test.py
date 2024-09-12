import chessLogic as chess
import copy

#board = chess.Board("r3k2r/Pppp1ppp/1b3nbN/nP6/BBP1P3/q4N2/Pp1P2PP/R2Q1RK1 w kq - 0 1")
#board = chess.Board("r3k2r/Pppp1ppp/1b3nbN/nP6/BBP1P3/q4N2/Pp1P2PP/R2Q1RK1 w kq - 0 1")
board = chess.Board("r4rk1/1pp1qppp/p1np1n2/2b1p1B1/2B1P1b1/P1NP1N2/1PP1QPPP/R4RK1 w - - 0 10")
#board = chess.Board()


import chess  # Importing python-chess

def perft(board, depth, path="", stats=None, verbose=False):
    """
    Performs a perft test on the given board.
    Returns the number of leaf nodes (positions) reached at the given depth.
    Tracks the sequence of moves that leads to a particular position using the 'path' variable.
    Also compares the moves with python-chess for debugging discrepancies.
    Does not work properly with promotions because they are not coded into the move, but instead hardcoded together with the UI sadly.
    """
    if stats is None:
        stats = {"checks": 0, "kingside_castles": 0, "queenside_castles": 0, "promotions": 0, "captures": 0}
    
    if depth == 0:
        return 1  

    nodes = 0

    fen = board.generate_fen()  
    py_chess_board = chess.Board(fen) 

    # Generate all moves for the current player in python-chess
    legal_moves_py_chess = [move.uci() for move in py_chess_board.legal_moves]
    
    # Generate all moves for the current player in the board
    custom_moves = []
    for row in range(8):
        for col in range(8):
            piece = board.piece_at(row, col)
            if piece and piece.color == board.current_turn:
                moves = piece.get_moves(board, row, col)
                for move in moves:
                    custom_moves.append(((row, col), move))

    # Compare the move counts and report discrepancies
    if len(custom_moves) != len(legal_moves_py_chess):
        print(f"Move count discrepancy! Custom engine generated {len(custom_moves)} moves, but python-chess generated {len(legal_moves_py_chess)} moves.")
        print(f"Discrepancy occurred after moves: {path}")
    
    # Check for missing moves in both engines
    custom_moves_uci = []
    for start_pos, move in custom_moves:
        move_uci = f"{board.square_to_algebraic(*start_pos)}{board.square_to_algebraic(*move)}"
        custom_moves_uci.append(move_uci)
        if move_uci not in legal_moves_py_chess:
            print(f"Missing move: {move_uci} in python-chess (present in custom engine).")

    for move in legal_moves_py_chess:
        if move not in custom_moves_uci:
            print(f"Missing move: {move} in custom engine (present in python-chess).")

    # Recursion for deeper depths
    for start_pos, move in custom_moves:
        new_path = path + " -> " + f"{board.square_to_algebraic(*start_pos)}{board.square_to_algebraic(*move)}"

        board_copy = board.generate_fen()  # Save the current game state

        # Simulate the move
        if board.move_piece(start_pos, move, None):
            # Update python-chess board to match the new FEN
            py_chess_board.set_fen(board_copy)
            
            # Recur for deeper depths
            nodes += perft(board, depth - 1, new_path, stats, verbose)

        # Restore the board to the original state
        board.load_fen(board_copy)
        py_chess_board.set_fen(fen)  # Restore python-chess to the original FEN as well

    return nodes


depth = 3  
stats = {"checks": 0, "kingside_castles": 0, "queenside_castles": 0, "promotions": 0, "captures": 0}

total_nodes = perft(board, depth, path="", verbose=True)

# Used previously, might reuse later, but not currently working
print(f"Total nodes: {total_nodes}")
print(f"Total checks: {stats['checks']}")
print(f"Kingside castles: {stats['kingside_castles']}")
print(f"Queenside castles: {stats['queenside_castles']}")
print(f"Promotions: {stats['promotions']}")
print(f"Captures: {stats['captures']}")

