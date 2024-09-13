from dataBase import db

class ChessGame(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # Unique game ID
    fen = db.Column(db.String, nullable=False)       # Current FEN string
    moves = db.Column(db.String, nullable=False)  # List of moves in UCI format
    game_status = db.Column(db.String(20), nullable=False, default='ongoing')  # Could be 'ongoing', 'checkmate', 'stalemate'
    opening_phase = db.Column(db.Boolean, nullable=False, default=True)  # Whether the game is in the opening phase
    player_color = db.Column(db.String(5), nullable=False)  # Color of the player