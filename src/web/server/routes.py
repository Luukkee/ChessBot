import sys, os
from models import *
from dataBase import app
from flask import abort, request, redirect
from flask import jsonify, json, url_for
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

# Now you can import modules from chessGame
from chessGame import Engine
from chessGame import Board
from chessGame import ChessNet
import torch

model_folder_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'model'))
model_file_path = os.path.join(model_folder_path, 'savedModels/updated_again_model_current.pth')

model = ChessNet()
model.load_state_dict(torch.load(model_file_path))
model.eval()

@app.route('/new_game/<player>', methods=['POST'])
def new_game(player):
    print(player)
    # Create a new game
    player_color = "white" if player=="1" else "black"
    game = ChessGame(fen=Board().generate_fen(), player_color=player_color)
    db.session.add(game)
    db.session.commit()

    return jsonify({"status": "success", "game_id": game.id, "fen": game.fen})

@app.route('/engine_move/<game_id>', methods=['PUT'])
def make_move(game_id):
    # Load the game from the database
    game = ChessGame.query.get_or_404(game_id)
    if not game:
        return jsonify({"status": "error", "message": "Game not found"}), 404
    if game.game_status != 'ongoing':
        return jsonify({"status": "error", "message": "Game is already over"}), 400

    board = Board(game.fen)
    print(game.fen)
    engine = Engine(color="white" if game.player_color=="black" else "black", opening_phase=game.opening_phase, played_moves=[] if not game.moves else game.moves.split(" ")[:-1])
    print(engine.played_moves)
    print(engine.opening_phase)
    print(engine.color)
    
    # Apply the move to the engine
    engine_move = engine.engine_move(board, model)
    print(engine_move)
    if not engine_move:
        return jsonify({"status": "error", "message": "No valid moves found"}), 400
    engine_m, move = engine_move
    move = move.uci()
    engine_start_pos, engine_end_pos = engine_m
    print(engine_start_pos, engine_end_pos)
    next_move = engine.update((engine_start_pos, engine_end_pos), board, True)
    if board.move_piece(engine_start_pos, engine_end_pos, None):
        game.fen = board.generate_fen()
        next_move = engine.played_moves[-1] if engine.opening_phase else next_move
        game.moves = (game.moves or '') + next_move + " "  # Update move history
        game.opening_phase = engine.opening_phase
        db.session.commit()

        return jsonify({"status": "success", "fen": game.fen, "next_move": move})
    else:
        return jsonify({"status": "error", "message": "Invalid move"}), 400
    
@app.route('/move/<game_id>', methods=['POST'])
def move(game_id):
    # Load the game from the database
    game = ChessGame.query.get_or_404(game_id)
    if not game:
        return jsonify({"status": "error", "message": "Game not found"}), 404
    if game.game_status != 'ongoing':
        return jsonify({"status": "error", "message": "Game is already over"}), 400

    board = Board(game.fen)
    move = request.json.get('move')
    move_data = move.get('move', {})
    from_square = move_data.get('from')  # E.g., 'e2'
    to_square = move_data.get('to')
    print(from_square, to_square)
    start_pos, end_pos = board.algebraic_to_index(from_square), board.algebraic_to_index(to_square)
    start_pos = (7-start_pos[0], start_pos[1])
    end_pos = (7-end_pos[0], end_pos[1])
    tmp_engine = Engine()
    print(start_pos, end_pos)
    update = tmp_engine.update((start_pos, end_pos), board, actual=True)
    if board.move_piece(start_pos, end_pos, None):
        game.fen = board.generate_fen()
        game.moves = (game.moves or '') + update + " " # Update move history
        del tmp_engine
        db.session.commit()

        return jsonify({"status": "success", "fen": game.fen})
    else:
        return jsonify({"status": "error", "message": "Invalid move"}), 400

@app.route('/game_status/<game_id>', methods=['GET'])
def game_status(game_id):
    # Load the game from the database
    game = ChessGame.query.get_or_404(game_id)
    if not game:
        return jsonify({"status": "error", "message": "Game not found"}), 404

    return jsonify({"status": "success", "game_status": game.game_status})

@app.route('/game/<game_id>', methods=['GET'])
def get_game(game_id):
    # Load the game from the database
    game = ChessGame.query.get_or_404(game_id)
    if not game:
        return jsonify({"status": "error", "message": "Game not found"}), 404

    return jsonify({"status": "success", "fen": game.fen, "moves": game.moves, "game_status": game.game_status})

#@app.route('/possible_moves/<game_id>', methods=['GET'])
#def possible_moves(game_id):
#    # Load the game from the database
#    game = ChessGame.query.get_or_404(game_id)
#    if not game:
#        return jsonify({"status": "error", "message": "Game not found"}), 404
#
#    board = Board(game.fen)
#    square = request.json.get('square')
#    row, col = square.get('row'), square.get('col')
#    piece = board.piece_at(row, col)
#    if not piece:
#        return jsonify({"status": "error", "message": "No piece at the specified square"}), 400
#    
#    moves = piece.get_moves(board, row, col)
#    return jsonify({"status": "success", "moves": moves})