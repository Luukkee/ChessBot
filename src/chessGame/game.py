import pygame
import sys
import chessLogic as chess
from engineIntegration import Engine

""""""""""""""""""
"  CHESS GAME    "
""""""""""""""""""

# Initialize Pygame
pygame.init()

# Define constants
WIDTH, HEIGHT = 800, 800
ROWS, COLS = 8, 8
SQUARE_SIZE = WIDTH // COLS

# Colors
WHITE = (240, 217, 181)  # Light beige
BLACK = (181, 136, 99)    # Dark brown
HIGHLIGHT_COLOR = (255, 0, 0)  # Red

# Load images
def load_images():
    pieces = ['king', 'queen', 'rook', 'bishop', 'knight', 'pawn']
    colors = ['white', 'black']
    images = {}
    for piece in pieces:
        for color in colors:
            images[f'{color}_{piece}'] = pygame.image.load(f'images/{color}_{piece}.png').convert_alpha()
    return images

# Draw board
def draw_board(win):
    for row in range(ROWS):
        for col in range(COLS):
            color = WHITE if (row + col) % 2 == 0 else BLACK
            pygame.draw.rect(win, color, (col*SQUARE_SIZE, row*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

# Draw pieces
def draw_pieces(win, board, images, dragging, selected_pos):
    for row, col in chess.SQUARES:
        if dragging and selected_pos == (row, col):
            continue  # Skip drawing the piece that is being dragged
        piece = board.piece_at(row, col)
        if piece:
            piece_image = images[f'{piece.color}_{piece.piece_type}']
            x = col * SQUARE_SIZE
            y = row * SQUARE_SIZE
            win.blit(piece_image, (x, y))

def draw_turn_indicator(win, current_turn):
    font = pygame.font.SysFont(None, 36)
    turn_text = font.render(f"Turn: {current_turn.capitalize()}", True, (0, 0, 0))
    win.blit(turn_text, (10, 10))

def draw_valid_moves(win, moves):
    for move in moves:
        row, col = move
        pygame.draw.circle(win, HIGHLIGHT_COLOR, (col * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2), 15)

def draw_promotion_window(win, board):
    #Choose promotion piece between queen, rook, bishop, knight
    font = pygame.font.SysFont(None, 36)
    text = font.render("Choose promotion piece", True, (0, 0, 0))
    win.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2))
    pieces = ['queen', 'rook', 'bishop', 'knight']
    for i, piece in enumerate(pieces):
        piece_image = pygame.image.load(f'images/white_{piece}.png').convert_alpha()
        x = WIDTH // 2 - (len(pieces) * SQUARE_SIZE) // 2 + i * SQUARE_SIZE
        y = HEIGHT // 2 + SQUARE_SIZE
        win.blit(piece_image, (x, y))
    pygame.display.flip()
    #click on piece to choose
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                posi = pygame.mouse.get_pos()
                x, y = posi
                for i, piece in enumerate(pieces):
                    if x > WIDTH // 2 - (len(pieces) * SQUARE_SIZE) // 2 + i * SQUARE_SIZE and x < WIDTH // 2 - (len(pieces) * SQUARE_SIZE) // 2 + (i + 1) * SQUARE_SIZE and y > HEIGHT // 2 + SQUARE_SIZE and y < HEIGHT // 2 + 2 * SQUARE_SIZE:
                        return piece
            if event.type == pygame.QUIT:
                running = False
    sys.exit()

def choose_color(win):
    font = pygame.font.SysFont(None, 48)
    white_text = font.render("Play as White", True, (0, 0, 0))
    black_text = font.render("Play as Black", True, (0, 0, 0))

    white_rect = white_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50))
    black_rect = black_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 50))

    while True:
        win.fill(WHITE)
        win.blit(white_text, white_rect)
        win.blit(black_text, black_rect)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if white_rect.collidepoint(pos):
                    return 'white'
                if black_rect.collidepoint(pos):
                    return 'black'

# Main function
def main():
    win = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('Chess')
    images = load_images()
    board = chess.Board()

    player_color = choose_color(win)
    engine_color = 'black' if player_color == 'white' else 'white'
    engine = Engine(color=engine_color, opening_phase=board.generate_fen()=="rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")
    # Main loop
    running = True
    selected_piece = None
    selected_pos = None
    dragging = False
    valid_moves = []

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if board.current_turn == player_color:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    col = pos[0] // SQUARE_SIZE
                    row = pos[1] // SQUARE_SIZE
                    if board.piece_at(row, col) and board.piece_at(row, col).color == board.current_turn:
                        selected_piece = board.piece_at(row, col)
                        selected_pos = (row, col)
                        valid_moves = selected_piece.get_moves(board, row, col)
                        dragging = True
                    elif selected_piece and selected_pos and not dragging and board.move_piece(selected_pos, (row, col), engine):
                        selected_piece = None
                        selected_pos = None
                        valid_moves = []
                    else:
                        selected_piece = None
                        selected_pos = None
                        valid_moves = []

                if event.type == pygame.MOUSEBUTTONUP:
                    if dragging:
                        pos = pygame.mouse.get_pos()
                        col = pos[0] // SQUARE_SIZE
                        row = pos[1] // SQUARE_SIZE
                        if board.move_piece(selected_pos, (row, col), engine):
                            selected_piece = None
                            selected_pos = None
                            valid_moves = []
                            dragging = False
                        else:
                            dragging = False
                    elif selected_piece and selected_pos: 
                        selected_piece = None
                        selected_pos = None
                        valid_moves = []

                if event.type == pygame.MOUSEMOTION and dragging:
                    pos = pygame.mouse.get_pos()
                    draw_board(win)
                    draw_pieces(win, board, images, dragging, selected_pos)
                    if selected_pos:
                        pygame.draw.rect(win, HIGHLIGHT_COLOR, (selected_pos[1] * SQUARE_SIZE, selected_pos[0] * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE), 3)
                        draw_valid_moves(win, valid_moves)
                    draw_turn_indicator(win, board.current_turn)
                    x, y = pos
                    piece_image = images[f'{selected_piece.color}_{selected_piece.piece_type}']
                    win.blit(piece_image, (x - SQUARE_SIZE // 2, y - SQUARE_SIZE // 2))
                    pygame.display.flip()
            
        # Redraw the board, pieces, and highlights in every loop iteration
        if not dragging:
            draw_board(win)
            if selected_pos:
                pygame.draw.rect(win, HIGHLIGHT_COLOR, (selected_pos[1] * SQUARE_SIZE, selected_pos[0] * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE), 3)
                draw_valid_moves(win, valid_moves)
            draw_pieces(win, board, images, dragging, selected_pos)
            draw_turn_indicator(win, board.current_turn)
            pygame.display.flip()

        if board.promotion:
            if board.current_turn == engine_color: # Counterintuitive, but move has passed to other party before this check
                
                piece = draw_promotion_window(win, board)
                print(piece)
            else:
                piece = 'queen'
            board.promotion_piece(piece)
            print(board.current_turn)

        # Handle the engine's turn
        if board.current_turn == engine_color:
            move, _ = engine.engine_move(board)
            engine_start_pos, engine_end_pos = move
            print(engine_start_pos, engine_end_pos)
            board.move_piece(engine_start_pos, engine_end_pos, None)

        # Promotion to choose piece
        if board.promotion:
            if board.current_turn == engine_color: # Counterintuitive, but move has passed to other party before this check
                
                piece = draw_promotion_window(win, board)
                print(piece)
            else:
                piece = 'queen'
            board.promotion_piece(piece)
            print(board.current_turn)

    pygame.quit()
    sys.exit()

if __name__ == '__main__':
    main()
