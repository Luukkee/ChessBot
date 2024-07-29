import os
import zipfile
import chess.pgn
from sqlalchemy import create_engine, Column, Integer, Text, Table, MetaData, text
from sqlalchemy.orm import declarative_base, sessionmaker
import io

"""
EXTREMELY INEFFICIENT WAY TO INSERT DATA INTO SQLITE DATABASE
1000 inserts per 30 seconds, but using for now to get some data into the database
"""


Base = declarative_base()

class ChessGame(Base):
    __tablename__ = 'games'
    id = Column(Integer, primary_key=True)
    pgn = Column(Text)

metadata = MetaData()
chess_game_table = Table('games', metadata,
                         Column('id', Integer, primary_key=True),
                         Column('pgn', Text))

# Define the path to the SQLite database
database_path = os.path.join(os.path.dirname(__file__), '..', 'chess_games.db')
engine = create_engine(f'sqlite:///{database_path}')
Base.metadata.create_all(engine)

def configure_database(engine):
    with engine.connect() as conn:
        conn.execute(text("PRAGMA journal_mode=WAL;"))
        conn.execute(text("PRAGMA synchronous=NORMAL;"))
        conn.execute(text("PRAGMA cache_size=100000;"))

configure_database(engine)

Session = sessionmaker(bind=engine)
session = Session()

def insert_games_core(games, conn):
    try:
        print(f"Inserting {len(games)} games into the database.")
        conn.execute(chess_game_table.insert(), games)
        conn.commit()
        print(f"Inserted {len(games)} games successfully.")
    except Exception as e:
        print(f"Error inserting games: {e}")

def process_zip(zip_path, engine, batch_size=1000):
    games_batch = []
    print(f"Processing zip file: {zip_path}")
    with zipfile.ZipFile(zip_path, 'r') as z:
        for file_name in z.namelist():
            print(f"Processing file: {file_name}")
            with z.open(file_name) as f:
                game_str = ""
                for line in io.TextIOWrapper(f, encoding='utf-8'):
                    game_str += line
                    if line.strip() == "" and game_str.strip():  # Empty line indicates end of game metadata
                        game = chess.pgn.read_game(io.StringIO(game_str))
                        if game is not None:
                            moves = ""
                            node = game
                            while node.variations:
                                next_node = node.variation(0)
                                moves += " " + node.board().san(next_node.move)
                                node = next_node
                            if moves.strip():
                                games_batch.append({"pgn": moves.strip()})
                            if len(games_batch) >= batch_size:
                                with engine.connect() as conn:
                                    insert_games_core(games_batch, conn)
                                games_batch.clear()
                        game_str = ""

                # Process any remaining game_str
                if game_str.strip():
                    game = chess.pgn.read_game(io.StringIO(game_str))
                    if game is not None:
                        moves = ""
                        node = game
                        while node.variations:
                            next_node = node.variation(0)
                            moves += " " + node.board().san(next_node.move)
                            node = next_node
                        if moves.strip():
                            games_batch.append({"pgn": moves.strip()})
                            print(f"Prepared game for insertion: {moves.strip()[:50]}...")

    # Insert any remaining games in the batch
    if games_batch:
        with engine.connect() as conn:
            insert_games_core(games_batch, conn)

# Define the path to the datasets
data_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'Datasets')
zip_files = [os.path.join(data_dir, f) for f in os.listdir(data_dir) if f.endswith('.zip')]

# Process all zip files
for zip_file in zip_files:
    process_zip(zip_file, engine)

print("Data processing complete.")
