from dataBase import db

class ChessGame(db.Model):
    id = db.Column(db.Integer, primary_key=True)  
    fen = db.Column(db.String, nullable=False)       
    moves = db.Column(db.String, nullable=True)  
    game_status = db.Column(db.String(20), nullable=False, default='ongoing')  
    opening_phase = db.Column(db.Boolean, nullable=False, default=True)  
    player_color = db.Column(db.String(5), nullable=False)  