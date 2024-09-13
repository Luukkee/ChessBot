from models import *
from dataBase import app
from flask import abort, request, redirect
from flask import jsonify, json, url_for
from chessGame import Engine
from chessGame import Board


@app.route('/new_game', methods=['POST'])
def new_game(player_color):
    # Create a new game
    game = ChessGame(fen=Board().generate_fen(), player_color=player_color)
    db.session.add(game)
    db.session.commit()

    return jsonify({"status": "success", "game_id": game.id, "fen": game.fen})

@app.route('/engine_move/<game_id>', methods=['POST'])
def make_move(game_id):
    # Load the game from the database
    game = ChessGame.query.get_or_404(game_id)
    if not game:
        return jsonify({"status": "error", "message": "Game not found"}), 404
    if game.game_status != 'ongoing':
        return jsonify({"status": "error", "message": "Game is already over"}), 400

    board = Board(game.fen)
    engine = Engine(color="white" if game.player_color=="black" else "black", opening_phase=game.opening_phase, played_moves=game.moves.split(" "))

    # Apply the move to the engine
    engine_start_pos, engine_end_pos = engine.engine_move(board)

    if board.move_piece(engine_start_pos, engine_end_pos, None):
        game.fen = board.generate_fen()
        game.moves = (game.moves or '') + engine.update((engine_start_pos, engine_end_pos), board, actual=False)  # Update move history
        db.session.commit()

        return jsonify({"status": "success", "fen": game.fen})
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
    start_pos = move.get('start_pos')
    end_pos = move.get('end_pos')

    if board.move_piece(start_pos, end_pos, None):
        game.fen = board.generate_fen()
        tmp_engine = Engine()
        game.moves = (game.moves or '') + tmp_engine.update((start_pos, end_pos), board, actual=True) # Update move history
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

@app.route('/possible_moves/<game_id>', methods=['GET'])
def possible_moves(game_id):
    # Load the game from the database
    game = ChessGame.query.get_or_404(game_id)
    if not game:
        return jsonify({"status": "error", "message": "Game not found"}), 404

    board = Board(game.fen)
    square = request.json.get('square')
    row, col = square.get('row'), square.get('col')
    piece = board.piece_at(row, col)
    if not piece:
        return jsonify({"status": "error", "message": "No piece at the specified square"}), 400
    
    moves = piece.get_moves(board, row, col)
    return jsonify({"status": "success", "moves": moves})