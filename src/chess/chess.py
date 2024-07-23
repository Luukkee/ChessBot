""""""""""""""""""
"  CHESS  LOGIC  "
""""""""""""""""""
SQUARES = [(x, y) for x in range(8) for y in range(8)]

class Piece:
    def __init__(self, color):
        self.color = color

    def get_moves(self, board, row, col):
        pass

class King(Piece):
    def __init__(self, color):
        super().__init__(color)
        self.piece_type = 'king'

    def get_moves(self, board, row, col):
        moves = []
        for i in range(-1, 2):
            for j in range(-1, 2):
                if i == 0 and j == 0:
                    continue
                new_row, new_col = row + i, col + j
                if 0 <= new_row < 8 and 0 <= new_col < 8:
                    piece = board.piece_at(new_row, new_col)
                    if not piece or piece.color != self.color:
                        moves.append((new_row, new_col))
        #Castling
        if board.castling_rights[self.color]['kingside']:
            if not board.piece_at(row, 5) and not board.piece_at(row, 6):
                rook = board.piece_at(row, 7)
                if rook and rook.piece_type == 'rook' and rook.color == self.color:
                    moves.append((row, 6))
        if board.castling_rights[self.color]['queenside']:
            if not board.piece_at(row, 1) and not board.piece_at(row, 2) and not board.piece_at(row, 3):
                rook = board.piece_at(row, 0)
                if rook and rook.piece_type == 'rook' and rook.color == self.color:
                    moves.append((row, 2))
        return moves

class Queen(Piece):
    def __init__(self, color):
        super().__init__(color)
        self.piece_type = 'queen'

    def get_moves(self, board, row, col):
        moves = []
        for i in range(-1, 2):
            for j in range(-1, 2):
                if i == 0 and j == 0:
                    continue
                new_row, new_col = row + i, col + j
                while 0 <= new_row < 8 and 0 <= new_col < 8:
                    piece = board.piece_at(new_row, new_col)
                    if not piece or piece.color != self.color:
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

    def get_moves(self, board, row, col):
        moves = []
        for i in range(-1, 2, 2):
            new_row, new_col = row + i, col
            while 0 <= new_row < 8:
                piece = board.piece_at(new_row, new_col)
                if not piece or piece.color != self.color:
                    moves.append((new_row, new_col))
                    if piece:
                        break
                else:
                    break
                new_row += i
        for i in range(-1, 2, 2):
            new_row, new_col = row, col + i
            while 0 <= new_col < 8:
                piece = board.piece_at(new_row, new_col)
                if not piece or piece.color != self.color:
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

    def get_moves(self, board, row, col):
        moves = []
        for i in range(-1, 2, 2):
            for j in range(-1, 2, 2):
                new_row, new_col = row + i, col + j
                while 0 <= new_row < 8 and 0 <= new_col < 8:
                    piece = board.piece_at(new_row, new_col)
                    if not piece or piece.color != self.color:
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

    def get_moves(self, board, row, col):
        moves = []
        for i in [-2, -1, 1, 2]:
            for j in [-2, -1, 1, 2]:
                if abs(i) != abs(j):
                    new_row, new_col = row + i, col + j
                    if 0 <= new_row < 8 and 0 <= new_col < 8:
                        piece = board.piece_at(new_row, new_col)
                        if not piece or piece.color != self.color:
                            moves.append((new_row, new_col))
        return moves

class Pawn(Piece):
    def __init__(self, color):
        super().__init__(color)
        self.piece_type = 'pawn'

    def get_moves(self, board, row, col):
        moves = []
        direction = -1 if self.color == 'white' else 1
        new_row, new_col = row + direction, col
        if 0 <= new_row < 8:
            piece = board.piece_at(new_row, new_col)
            if not piece:
                moves.append((new_row, new_col))
                if (row == 1 and self.color == 'black') or (row == 6 and self.color == 'white'):
                    new_row += direction
                    piece = board.piece_at(new_row, new_col)
                    if not piece:
                        moves.append((new_row, new_col))
        for i in [-1, 1]:
            #en passant
            if board.en_passant_target and board.en_passant_target == (row + direction, col + i):
                moves.append((row + direction, col + i))
            new_row, new_col = row + direction, col + i
            if 0 <= new_row < 8 and 0 <= new_col < 8:
                piece = board.piece_at(new_row, new_col)
                if piece and piece.color != self.color:
                    moves.append((new_row, new_col))
        return moves

class Board:
    def __init__(self):
        self.board = self.create_board()
        self.current_turn = 'white'
        self.en_passant_target = None
        self.promotion = None
        self.castling_rights = {'white': {'kingside': True, 'queenside': True},
                                'black': {'kingside': True, 'queenside': True}}
    def create_board(self):
        # Create an 8x8 board with pieces placed in starting positions
        board = [[None for _ in range(8)] for _ in range(8)]
        # Place pieces on the board (this is just an example)
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

    def move_piece(self, start_pos, end_pos):
        piece = self.piece_at(*start_pos)
        #print(piece)

        if piece and piece.color == self.current_turn:
            if end_pos in piece.get_moves(self, *start_pos):
                self.handle_special_moves(piece, start_pos, end_pos)
                self.board[end_pos[0]][end_pos[1]] = piece
                self.board[start_pos[0]][start_pos[1]] = None
                self.current_turn = 'black' if self.current_turn == 'white' else 'white'
                print(self.en_passant_target)

                if self.is_in_check(self.current_turn):
                    print(f"Check! {self.current_turn} is in check.")
                return True
        return False

    def is_valid_move(self, start_pos, end_pos):
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
        print(end_pos)
        #takes with en passant
        if piece.piece_type == 'pawn' and end_pos == self.en_passant_target:
            self.board[start_pos[0]][end_pos[1]] = None
        #Handle en passant
        if piece.piece_type == 'pawn' and abs(start_pos[0] - end_pos[0]) == 2:
            self.en_passant_target = ((start_pos[0] + end_pos[0]) // 2, start_pos[1])
        else:
            self.en_passant_target = None
        #Promotion, choose queen for now
        #TODO: Add a way to choose promotion piece
        if piece.piece_type == 'pawn' and (end_pos[0] == 0 or end_pos[0] == 7):
            self.promotion = end_pos
        #Handle castling
        if piece.piece_type == 'king' and abs(start_pos[1] - end_pos[1]) == 2:
            if end_pos[1] == 6:
                self.board[end_pos[0]][5] = self.board[end_pos[0]][7]
                self.board[end_pos[0]][7] = None
            elif end_pos[1] == 2:
                self.board[end_pos[0]][3] = self.board[end_pos[0]][0]
                self.board[end_pos[0]][0] = None
        #Update castling rights
        if piece.piece_type == 'rook' and start_pos[1] == 0:
            self.castling_rights[piece.color]['queenside'] = False
        elif piece.piece_type == 'rook' and start_pos[1] == 7:
            self.castling_rights[piece.color]['kingside'] = False
        elif piece.piece_type == 'king':
            self.castling_rights[piece.color]['kingside'] = False
            self.castling_rights[piece.color]['queenside'] = False


    #Handle check and
    def is_under_attack(self, row, col, color):
        opponent_color = 'black' if color == 'white' else 'white'
        for r in range(8):
            for c in range(8):
                piece = self.piece_at(r, c)
                if piece and piece.color == opponent_color:
                    if (row, col) in piece.get_moves(self, r, c):
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
        