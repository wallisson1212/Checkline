"""
XADREZ vs IA
Sistema de xadrez com inteligência artificial

Como usar:
    python play_chess.py [dificuldade] [cor]
    
Exemplos:
    python play_chess.py easy white      # IA Fácil, você com peças brancas
    python play_chess.py medium black    # IA Médio, você com peças pretas
    python play_chess.py hard white      # IA Difícil, você com peças brancas

Dificuldades: easy (aleatória), medium (3 profundidade), hard (5 profundidade)
Cores: white (brancas/douradas), black (pretas)

Controles:
    - Clique para selecionar e mover peças
    - ESC para sair
    - N para novo jogo
    - U para desfazer movimento
"""

import os
import pygame as pg
from enum import Enum
from typing import List, Tuple, Optional, Set


class PieceType(Enum):
    PAWN = 'pw'
    KNIGHT = 'kn'
    BISHOP = 'bs'
    ROOK = 'rk'
    QUEEN = 'qn'
    KING = 'kg'

class Color(Enum):
    WHITE = 'w'
    BLACK = 'b'

class Piece:
    def __init__(self, color: Color, piece_type: PieceType):
        self.color = color
        self.piece_type = piece_type
        self.has_moved = False
    
    def __repr__(self):
        return f"{self.color.value}_{self.piece_type.value}"
    
    def __eq__(self, other):
        if isinstance(other, str):
            return repr(self) == other
        return isinstance(other, Piece) and self.color == other.color and self.piece_type == other.piece_type

class Board:
    def __init__(self):
        self.grid = [[None for _ in range(8)] for _ in range(8)]
        self.initialize_board()
        self.move_history = []
        self.white_king_moved = False
        self.black_king_moved = False
        self.white_rook_a_moved = False
        self.white_rook_h_moved = False
        self.black_rook_a_moved = False
        self.black_rook_h_moved = False
        
    def initialize_board(self):
        # Peças pretas
        self.grid[0] = [
            Piece(Color.BLACK, PieceType.ROOK),
            Piece(Color.BLACK, PieceType.KNIGHT),
            Piece(Color.BLACK, PieceType.BISHOP),
            Piece(Color.BLACK, PieceType.QUEEN),
            Piece(Color.BLACK, PieceType.KING),
            Piece(Color.BLACK, PieceType.BISHOP),
            Piece(Color.BLACK, PieceType.KNIGHT),
            Piece(Color.BLACK, PieceType.ROOK),
        ]
        # Peões pretos
        for x in range(8):
            self.grid[1][x] = Piece(Color.BLACK, PieceType.PAWN)
        
        # Peões brancos
        for x in range(8):
            self.grid[6][x] = Piece(Color.WHITE, PieceType.PAWN)
        
        # Peças brancas
        self.grid[7] = [
            Piece(Color.WHITE, PieceType.ROOK),
            Piece(Color.WHITE, PieceType.KNIGHT),
            Piece(Color.WHITE, PieceType.BISHOP),
            Piece(Color.WHITE, PieceType.QUEEN),
            Piece(Color.WHITE, PieceType.KING),
            Piece(Color.WHITE, PieceType.BISHOP),
            Piece(Color.WHITE, PieceType.KNIGHT),
            Piece(Color.WHITE, PieceType.ROOK),
        ]
    
    def get_piece(self, x: int, y: int) -> Optional[Piece]:
        if 0 <= x < 8 and 0 <= y < 8:
            return self.grid[y][x]
        return None
    
    def set_piece(self, x: int, y: int, piece: Optional[Piece]):
        if 0 <= x < 8 and 0 <= y < 8:
            self.grid[y][x] = piece
    
    def is_empty(self, x: int, y: int) -> bool:
        return self.get_piece(x, y) is None
    
    def find_king(self, color: Color) -> Tuple[int, int]:
        for y in range(8):
            for x in range(8):
                piece = self.get_piece(x, y)
                if piece and piece.color == color and piece.piece_type == PieceType.KING:
                    return (x, y)
        return None

class ChessGame:
    def __init__(self, ai_enabled: bool = True, ai_difficulty: str = 'medium', player_color: Color = Color.WHITE):
        pg.init()
        self.base_dir = os.path.dirname(os.path.abspath(__file__))
        
        # Colors - Xadrez clássico: Dourado e Preto
        self.DARK_COLOR = (139, 69, 19)      # Marrom escuro (preto do xadrez)
        self.LIGHT_COLOR = (240, 217, 181)   # Bege/Dourado (claro do xadrez)
        self.HIGHLIGHT_COLOR = (0, 0, 0, 50)
        
        # Display
        self.WIDTH = 800
        self.HEIGHT = 800
        self.SQUARE_SIZE = 100
        self.window = pg.display.set_mode((self.WIDTH, self.HEIGHT))
        pg.display.set_caption('Xadrez vs IA')
        
        # Font
        self.font = pg.font.SysFont("Courier New", 25, bold=True)
        
        # Clock
        self.clock = pg.time.Clock()
        
        # Game state
        self.board = Board()
        self.current_player = Color.WHITE
        self.selected_square = None
        self.valid_moves = set()
        self.game_over = False
        self.winner = None
        self.en_passant_target = None
        self.last_click_status = (False, False, False)
        
        # AI configuration
        self.ai_enabled = ai_enabled
        self.player_color = player_color
        self.ai_color = Color.BLACK if player_color == Color.WHITE else Color.WHITE
        self.ai = ChessAI(ai_difficulty) if ai_enabled else None
        self.ai_thinking = False
        
        # Configurar tempo de resposta da IA baseado na dificuldade
        self.ai_response_time = {
            'easy': 15,      # ~250ms (rápido)
            'medium': 30,    # ~500ms (normal)
            'hard': 60       # ~1s (pensativo)
        }.get(ai_difficulty, 30)
        
        # Load piece images
        self.piece_images = self.load_piece_images()
        
        # Sounds
        self.sounds = self.load_sounds()
    
    def load_piece_images(self):
        images = {}
        pieces_files = {
            'pawn': ('pawn white.png', 'pawn black.png'),
            'knight': ('knight white.png', 'knight black.png'),
            'bishop': ('bishop white.png', 'bishop black.png'),
            'rook': ('rook white.png', 'rook black.png'),
            'queen': ('queen white.png', 'queen black.png'),
            'king': ('king white.png', 'king black.png'),
        }
        
        for piece_name, (white_file, black_file) in pieces_files.items():
            white_path = os.path.join(self.base_dir, white_file)
            black_path = os.path.join(self.base_dir, black_file)
            
            if os.path.exists(white_path):
                white_img = pg.image.load(white_path)
                images[f'w_{piece_name}'] = pg.transform.scale(white_img, (self.SQUARE_SIZE, self.SQUARE_SIZE))
            
            if os.path.exists(black_path):
                black_img = pg.image.load(black_path)
                images[f'b_{piece_name}'] = pg.transform.scale(black_img, (self.SQUARE_SIZE, self.SQUARE_SIZE))
        
        return images
    
    def load_sounds(self):
        sounds = {}
        try:
            pg.mixer.init()
            sound_files = {'move': 'move.wav', 'check': 'check.wav', 'mate': 'mate.wav'}
            for name, filename in sound_files.items():
                path = os.path.join(self.base_dir, 'sounds', filename)
                if os.path.exists(path):
                    sounds[name] = pg.mixer.Sound(path)
        except:
            pass
        return sounds
    
    def play_sound(self, sound_name: str):
        if sound_name in self.sounds and self.sounds[sound_name]:
            try:
                self.sounds[sound_name].play()
            except:
                pass
    
    def detect_click(self, input_status):
        if self.last_click_status == input_status:
            return (False, False, False)
        
        left_click = (self.last_click_status[0] == False and input_status[0] == True)
        middle_click = (self.last_click_status[1] == False and input_status[1] == True)
        right_click = (self.last_click_status[2] == False and input_status[2] == True)
        
        self.last_click_status = input_status
        return (left_click, middle_click, right_click)
    
    def pos_to_square(self, pos: Tuple[int, int]) -> Optional[Tuple[int, int]]:
        x, y = pos
        if 0 <= x < self.WIDTH and 0 <= y < self.HEIGHT:
            col = x // self.SQUARE_SIZE
            row = y // self.SQUARE_SIZE
            return (col, row)
        return None
    
    def get_pawn_moves(self, x: int, y: int, piece: Piece) -> Set[Tuple[int, int]]:
        moves = set()
        direction = -1 if piece.color == Color.WHITE else 1
        start_row = 6 if piece.color == Color.WHITE else 1
        
        # Move forward one square
        next_y = y + direction
        if 0 <= next_y < 8 and self.board.is_empty(x, next_y):
            moves.add((x, next_y))
            
            # Move forward two squares from starting position
            if y == start_row:
                next_next_y = y + 2 * direction
                if self.board.is_empty(x, next_next_y):
                    moves.add((x, next_next_y))
        
        # Capture diagonally
        for dx in [-1, 1]:
            capture_x = x + dx
            capture_y = y + direction
            if 0 <= capture_x < 8 and 0 <= capture_y < 8:
                target = self.board.get_piece(capture_x, capture_y)
                if target and target.color != piece.color:
                    moves.add((capture_x, capture_y))
                
                # En passant
                if self.en_passant_target == (capture_x, capture_y):
                    moves.add((capture_x, capture_y))
        
        return moves
    
    def get_knight_moves(self, x: int, y: int, piece: Piece) -> Set[Tuple[int, int]]:
        moves = set()
        knight_moves = [
            (-2, -1), (-2, 1), (-1, -2), (-1, 2),
            (1, -2), (1, 2), (2, -1), (2, 1)
        ]
        
        for dx, dy in knight_moves:
            nx, ny = x + dx, y + dy
            if 0 <= nx < 8 and 0 <= ny < 8:
                target = self.board.get_piece(nx, ny)
                if target is None or target.color != piece.color:
                    moves.add((nx, ny))
        
        return moves
    
    def get_bishop_moves(self, x: int, y: int, piece: Piece) -> Set[Tuple[int, int]]:
        moves = set()
        directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
        
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            while 0 <= nx < 8 and 0 <= ny < 8:
                target = self.board.get_piece(nx, ny)
                if target is None:
                    moves.add((nx, ny))
                elif target.color != piece.color:
                    moves.add((nx, ny))
                    break
                else:
                    break
                nx += dx
                ny += dy
        
        return moves
    
    def get_rook_moves(self, x: int, y: int, piece: Piece) -> Set[Tuple[int, int]]:
        moves = set()
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            while 0 <= nx < 8 and 0 <= ny < 8:
                target = self.board.get_piece(nx, ny)
                if target is None:
                    moves.add((nx, ny))
                elif target.color != piece.color:
                    moves.add((nx, ny))
                    break
                else:
                    break
                nx += dx
                ny += dy
        
        return moves
    
    def get_queen_moves(self, x: int, y: int, piece: Piece) -> Set[Tuple[int, int]]:
        return self.get_rook_moves(x, y, piece) | self.get_bishop_moves(x, y, piece)
    
    def get_king_moves(self, x: int, y: int, piece: Piece) -> Set[Tuple[int, int]]:
        moves = set()
        
        # Normal king moves
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if dx == 0 and dy == 0:
                    continue
                nx, ny = x + dx, y + dy
                if 0 <= nx < 8 and 0 <= ny < 8:
                    target = self.board.get_piece(nx, ny)
                    if target is None or target.color != piece.color:
                        moves.add((nx, ny))
        
        # Castling
        if piece.color == Color.WHITE and not self.board.white_king_moved and y == 7 and x == 4:
            # Kingside castling
            if not self.board.white_rook_h_moved and self.board.is_empty(5, 7) and self.board.is_empty(6, 7):
                rook = self.board.get_piece(7, 7)
                if rook and rook.piece_type == PieceType.ROOK:
                    moves.add((6, 7))
            
            # Queenside castling
            if not self.board.white_rook_a_moved and self.board.is_empty(1, 7) and self.board.is_empty(2, 7) and self.board.is_empty(3, 7):
                rook = self.board.get_piece(0, 7)
                if rook and rook.piece_type == PieceType.ROOK:
                    moves.add((2, 7))
        
        elif piece.color == Color.BLACK and not self.board.black_king_moved and y == 0 and x == 4:
            # Kingside castling
            if not self.board.black_rook_h_moved and self.board.is_empty(5, 0) and self.board.is_empty(6, 0):
                rook = self.board.get_piece(7, 0)
                if rook and rook.piece_type == PieceType.ROOK:
                    moves.add((6, 0))
            
            # Queenside castling
            if not self.board.black_rook_a_moved and self.board.is_empty(1, 0) and self.board.is_empty(2, 0) and self.board.is_empty(3, 0):
                rook = self.board.get_piece(0, 0)
                if rook and rook.piece_type == PieceType.ROOK:
                    moves.add((2, 0))
        
        return moves
    
    def get_valid_moves(self, x: int, y: int) -> Set[Tuple[int, int]]:
        piece = self.board.get_piece(x, y)
        if piece is None or piece.color != self.current_player:
            return set()
        
        if piece.piece_type == PieceType.PAWN:
            moves = self.get_pawn_moves(x, y, piece)
        elif piece.piece_type == PieceType.KNIGHT:
            moves = self.get_knight_moves(x, y, piece)
        elif piece.piece_type == PieceType.BISHOP:
            moves = self.get_bishop_moves(x, y, piece)
        elif piece.piece_type == PieceType.ROOK:
            moves = self.get_rook_moves(x, y, piece)
        elif piece.piece_type == PieceType.QUEEN:
            moves = self.get_queen_moves(x, y, piece)
        elif piece.piece_type == PieceType.KING:
            moves = self.get_king_moves(x, y, piece)
        else:
            moves = set()
        
        # Filter moves that leave king in check
        legal_moves = set()
        for move_x, move_y in moves:
            if not self.move_leaves_king_in_check(x, y, move_x, move_y):
                legal_moves.add((move_x, move_y))
        
        return legal_moves
    
    def is_under_attack(self, x: int, y: int, by_color: Color) -> bool:
        for row in range(8):
            for col in range(8):
                piece = self.board.get_piece(col, row)
                if piece and piece.color == by_color:
                    moves = self.get_pseudo_legal_moves(col, row, piece)
                    if (x, y) in moves:
                        return True
        return False
    
    def get_pseudo_legal_moves(self, x: int, y: int, piece: Piece) -> Set[Tuple[int, int]]:
        if piece.piece_type == PieceType.PAWN:
            return self.get_pawn_moves(x, y, piece)
        elif piece.piece_type == PieceType.KNIGHT:
            return self.get_knight_moves(x, y, piece)
        elif piece.piece_type == PieceType.BISHOP:
            return self.get_bishop_moves(x, y, piece)
        elif piece.piece_type == PieceType.ROOK:
            return self.get_rook_moves(x, y, piece)
        elif piece.piece_type == PieceType.QUEEN:
            return self.get_queen_moves(x, y, piece)
        elif piece.piece_type == PieceType.KING:
            moves = set()
            for dx in [-1, 0, 1]:
                for dy in [-1, 0, 1]:
                    if dx == 0 and dy == 0:
                        continue
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < 8 and 0 <= ny < 8:
                        target = self.board.get_piece(nx, ny)
                        if target is None or target.color != piece.color:
                            moves.add((nx, ny))
            return moves
        return set()
    
    def move_leaves_king_in_check(self, from_x: int, from_y: int, to_x: int, to_y: int) -> bool:
        # Save current state
        piece = self.board.get_piece(from_x, from_y)
        captured = self.board.get_piece(to_x, to_y)
        en_passant_capture = False
        
        # Make the move
        self.board.set_piece(to_x, to_y, piece)
        self.board.set_piece(from_x, from_y, None)
        
        # Handle en passant capture
        if piece.piece_type == PieceType.PAWN and self.en_passant_target == (to_x, to_y):
            ep_x, ep_y = to_x, to_y
            direction = -1 if piece.color == Color.WHITE else 1
            ep_y -= direction
            ep_piece = self.board.get_piece(ep_x, ep_y)
            self.board.set_piece(ep_x, ep_y, None)
            en_passant_capture = True
        
        # Check if king is in check
        king_pos = self.board.find_king(piece.color)
        opponent_color = Color.BLACK if piece.color == Color.WHITE else Color.WHITE
        in_check = self.is_under_attack(king_pos[0], king_pos[1], opponent_color)
        
        # Restore state
        self.board.set_piece(from_x, from_y, piece)
        self.board.set_piece(to_x, to_y, captured)
        if en_passant_capture:
            self.board.set_piece(ep_x, ep_y, ep_piece)
        
        return in_check
    
    def make_move(self, from_x: int, from_y: int, to_x: int, to_y: int) -> bool:
        piece = self.board.get_piece(from_x, from_y)
        if piece is None or piece.color != self.current_player:
            return False
        
        if (to_x, to_y) not in self.get_valid_moves(from_x, from_y):
            return False
        
        # Save move history
        captured = self.board.get_piece(to_x, to_y)
        self.board.move_history.append((from_x, from_y, to_x, to_y, captured))
        
        # Move piece
        self.board.set_piece(to_x, to_y, piece)
        self.board.set_piece(from_x, from_y, None)
        
        # Handle special moves
        # En passant capture
        if piece.piece_type == PieceType.PAWN and self.en_passant_target == (to_x, to_y):
            direction = -1 if piece.color == Color.WHITE else 1
            capture_y = to_y - direction
            self.board.set_piece(to_x, capture_y, None)
        
        # Pawn promotion
        if piece.piece_type == PieceType.PAWN:
            if (piece.color == Color.WHITE and to_y == 0) or (piece.color == Color.BLACK and to_y == 7):
                piece.piece_type = PieceType.QUEEN
            
            # Check for en passant possibility
            if abs(to_y - from_y) == 2:
                self.en_passant_target = (to_x, from_y + (to_y - from_y) // 2)
            else:
                self.en_passant_target = None
        else:
            self.en_passant_target = None
        
        # Castling
        if piece.piece_type == PieceType.KING:
            if piece.color == Color.WHITE:
                self.board.white_king_moved = True
            else:
                self.board.black_king_moved = True
            
            # Move rook for castling
            if from_x == 4 and to_x == 6:  # Kingside
                rook = self.board.get_piece(7, to_y)
                if rook and rook.piece_type == PieceType.ROOK:
                    self.board.set_piece(7, to_y, None)
                    self.board.set_piece(5, to_y, rook)
                    if piece.color == Color.WHITE:
                        self.board.white_rook_h_moved = True
                    else:
                        self.board.black_rook_h_moved = True
            
            elif from_x == 4 and to_x == 2:  # Queenside
                rook = self.board.get_piece(0, to_y)
                if rook and rook.piece_type == PieceType.ROOK:
                    self.board.set_piece(0, to_y, None)
                    self.board.set_piece(3, to_y, rook)
                    if piece.color == Color.WHITE:
                        self.board.white_rook_a_moved = True
                    else:
                        self.board.black_rook_a_moved = True
        
        elif piece.piece_type == PieceType.ROOK:
            if piece.color == Color.WHITE:
                if from_x == 0:
                    self.board.white_rook_a_moved = True
                elif from_x == 7:
                    self.board.white_rook_h_moved = True
            else:
                if from_x == 0:
                    self.board.black_rook_a_moved = True
                elif from_x == 7:
                    self.board.black_rook_h_moved = True
        
        # Play sound
        if captured:
            self.play_sound('move')
        else:
            self.play_sound('move')
        
        # Switch player
        self.current_player = Color.BLACK if self.current_player == Color.WHITE else Color.WHITE
        
        # Check game state
        self.update_game_state()
        
        return True
    
    def has_legal_moves(self, color: Color) -> bool:
        for y in range(8):
            for x in range(8):
                piece = self.board.get_piece(x, y)
                if piece and piece.color == color:
                    if self.get_valid_moves(x, y):
                        return True
        return False
    
    def is_in_check(self, color: Color) -> bool:
        king_pos = self.board.find_king(color)
        if king_pos is None:
            return False
        opponent_color = Color.BLACK if color == Color.WHITE else Color.WHITE
        return self.is_under_attack(king_pos[0], king_pos[1], opponent_color)
    
    def update_game_state(self):
        current_in_check = self.is_in_check(self.current_player)
        has_moves = self.has_legal_moves(self.current_player)
        
        if not has_moves:
            self.game_over = True
            if current_in_check:
                opponent = Color.WHITE if self.current_player == Color.BLACK else Color.BLACK
                self.winner = opponent
                self.play_sound('mate')
            else:
                self.play_sound('move')
        elif current_in_check:
            self.play_sound('check')
    
    def move_piece(self, from_x: int, from_y: int, to_x: int, to_y: int, is_check: bool = True) -> bool:
        """Move a piece from one position to another (used by AI and validation)"""
        return self.make_move(from_x, from_y, to_x, to_y)
    
    def get_piece_moves(self, x: int, y: int) -> Set[Tuple[int, int]]:
        """Get all valid moves for a piece (used by AI)"""
        return self.get_valid_moves(x, y)
    
    def handle_click(self, pos: Tuple[int, int]):
        square = self.pos_to_square(pos)
        if square is None:
            return
        
        x, y = square
        piece = self.board.get_piece(x, y)
        
        if self.selected_square is None:
            # Select piece
            if piece and piece.color == self.current_player:
                self.selected_square = square
                self.valid_moves = self.get_valid_moves(x, y)
        else:
            # Try to move
            if square == self.selected_square:
                # Deselect
                self.selected_square = None
                self.valid_moves = set()
            else:
                from_x, from_y = self.selected_square
                if self.make_move(from_x, from_y, x, y):
                    self.selected_square = None
                    self.valid_moves = set()
                else:
                    # Select new piece
                    if piece and piece.color == self.current_player:
                        self.selected_square = square
                        self.valid_moves = self.get_valid_moves(x, y)
                    else:
                        self.selected_square = None
                        self.valid_moves = set()
    
    def draw_board(self):
        for y in range(8):
            for x in range(8):
                rect = pg.Rect(x * self.SQUARE_SIZE, y * self.SQUARE_SIZE, self.SQUARE_SIZE, self.SQUARE_SIZE)
                if (x + y) % 2 == 0:
                    pg.draw.rect(self.window, self.LIGHT_COLOR, rect)
                else:
                    pg.draw.rect(self.window, self.DARK_COLOR, rect)
        
        # Draw coordinates
        for x in range(8):
            col_label = chr(ord('a') + x)
            text = self.font.render(col_label, True, self.DARK_COLOR)
            self.window.blit(text, (x * self.SQUARE_SIZE + 75, 775))
        
        for y in range(8):
            row_label = str(8 - y)
            text = self.font.render(row_label, True, self.DARK_COLOR)
            self.window.blit(text, (5, y * self.SQUARE_SIZE + 5))
    
    def draw_pieces(self):
        for y in range(8):
            for x in range(8):
                piece = self.board.get_piece(x, y)
                if piece:
                    color_str = piece.color.value
                    piece_type = piece.piece_type.value
                    type_names = {
                        'pw': 'pawn',
                        'kn': 'knight',
                        'bs': 'bishop',
                        'rk': 'rook',
                        'qn': 'queen',
                        'kg': 'king'
                    }
                    image_key = f"{color_str}_{type_names[piece_type]}"
                    if image_key in self.piece_images:
                        self.window.blit(self.piece_images[image_key], 
                                       (x * self.SQUARE_SIZE, y * self.SQUARE_SIZE))
    
    def draw_valid_moves(self):
        if self.selected_square:
            x, y = self.selected_square
            # Highlight selected square
            rect = pg.Rect(x * self.SQUARE_SIZE, y * self.SQUARE_SIZE, self.SQUARE_SIZE, self.SQUARE_SIZE)
            s = pg.Surface((self.SQUARE_SIZE, self.SQUARE_SIZE), pg.SRCALPHA)
            s.fill((100, 100, 100, 100))
            self.window.blit(s, rect)
            
            # Draw valid moves
            for move_x, move_y in self.valid_moves:
                target = self.board.get_piece(move_x, move_y)
                if target:
                    # Capture move
                    pg.draw.circle(self.window, (200, 100, 100), 
                                 (move_x * self.SQUARE_SIZE + self.SQUARE_SIZE // 2, 
                                  move_y * self.SQUARE_SIZE + self.SQUARE_SIZE // 2), 10)
                else:
                    # Empty square move
                    pg.draw.circle(self.window, (150, 150, 150), 
                                 (move_x * self.SQUARE_SIZE + self.SQUARE_SIZE // 2, 
                                  move_y * self.SQUARE_SIZE + self.SQUARE_SIZE // 2), 5)
    
    def draw_game_status(self):
        # Status da IA
        if self.ai_enabled:
            ai_label = "IA" if self.current_player == self.ai_color else "Você"
            time_text = self.font.render(f"Vez: {ai_label}", True, self.DARK_COLOR)
            self.window.blit(time_text, (10, 10))
        
        # Dificuldade da IA
        if self.ai_enabled:
            difficulty_labels = {
                'easy': '🎮 Fácil',
                'medium': '🤖 Médio',
                'hard': '🧠 Difícil'
            }
            diff_text = self.font.render(difficulty_labels.get(self.ai.difficulty, 'Médio'), True, self.DARK_COLOR)
            self.window.blit(diff_text, (600, 10))
        
        if self.game_over:
            if self.winner:
                text = f"Xeque-mate - {self.winner.name.capitalize()} venceu!"
            else:
                text = "Afogamento - Empate!"
            status_text = self.font.render(text, True, (255, 0, 0))
            self.window.blit(status_text, (10, 50))
        else:
            if self.is_in_check(self.current_player):
                text = f"Xeque - {self.current_player.name.capitalize()}"
                status_text = self.font.render(text, True, (255, 100, 100))
                self.window.blit(status_text, (10, 50))
    
    def draw(self):
        self.draw_board()
        self.draw_pieces()
        self.draw_valid_moves()
        self.draw_game_status()
        pg.display.flip()
    
    def run(self):
        running = True
        ai_move_timer = 0
        while running:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    running = False
                elif event.type == pg.MOUSEBUTTONDOWN:
                    if event.button == 1 and not self.game_over and self.current_player == self.player_color:
                        self.handle_click(pg.mouse.get_pos())
                elif event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        running = False
                    elif event.key == pg.K_n:
                        self.__init__()
                    elif event.key == pg.K_u:
                        self.undo_move()
            
            # AI faz seu movimento
            if self.ai_enabled and self.current_player == self.ai_color and not self.game_over:
                ai_move_timer += 1
                # Aguarda tempo configurado pela dificuldade
                if ai_move_timer >= self.ai_response_time:
                    ai_move_timer = 0
                    ai_move = self.ai.get_best_move(self, self.ai_color)
                    if ai_move:
                        from_x, from_y, to_x, to_y = ai_move
                        self.make_move(from_x, from_y, to_x, to_y)
            
            self.clock.tick(60)
            self.draw()
        
        pg.quit()
    
    def undo_move(self):
        if not self.board.move_history:
            return
        
        from_x, from_y, to_x, to_y, captured = self.board.move_history.pop()
        piece = self.board.get_piece(to_x, to_y)
        
        self.board.set_piece(from_x, from_y, piece)
        self.board.set_piece(to_x, to_y, captured)
        
        self.current_player = Color.BLACK if self.current_player == Color.WHITE else Color.WHITE
        self.selected_square = None
        self.valid_moves = set()
        self.game_over = False
        self.winner = None

class ChessAI:
    """Inteligência Artificial para jogar Xadrez"""
    
    # Valores das peças para avaliação
    PIECE_VALUES = {
        PieceType.PAWN: 1,
        PieceType.KNIGHT: 3,
        PieceType.BISHOP: 3,
        PieceType.ROOK: 5,
        PieceType.QUEEN: 9,
        PieceType.KING: 1000
    }
    
    def __init__(self, difficulty: str = 'medium'):
        """
        Inicializa a IA
        difficulty: 'easy', 'medium' ou 'hard'
        """
        self.difficulty = difficulty
        self.max_depth = {
            'easy': 1,
            'medium': 3,
            'hard': 5
        }.get(difficulty, 3)
        self.eval_count = 0
    
    def get_best_move(self, game: 'ChessGame', color: Color) -> Optional[Tuple[int, int, int, int]]:
        """Retorna o melhor movimento para a cor dada"""
        import random
        
        # Coletar todos os movimentos possíveis
        all_moves = []
        for y in range(8):
            for x in range(8):
                piece = game.board.get_piece(x, y)
                if piece and piece.color == color:
                    moves = game.get_piece_moves(x, y)
                    for to_x, to_y in moves:
                        all_moves.append((x, y, to_x, to_y))
        
        if not all_moves:
            return None
        
        # Fácil: retorna um movimento aleatório
        if self.difficulty == 'easy':
            return random.choice(all_moves)
        
        # Médio e Difícil: usar minimax
        best_move = all_moves[0]
        best_score = float('-inf')
        
        for from_x, from_y, to_x, to_y in all_moves:
            # Fazer o movimento temporariamente
            captured_piece = game.board.get_piece(to_x, to_y)
            piece = game.board.get_piece(from_x, from_y)
            
            # Salvar estado
            old_current_player = game.current_player
            old_game_over = game.game_over
            old_winner = game.winner
            
            # Executar movimento manualmente sem registrar no histórico
            game.board.set_piece(to_x, to_y, piece)
            game.board.set_piece(from_x, from_y, None)
            game.current_player = Color.BLACK if game.current_player == Color.WHITE else Color.WHITE
            
            # Avaliar posição
            score = self._minimax(game, self.max_depth - 1, False, color)
            
            # Restaurar estado
            game.board.set_piece(from_x, from_y, piece)
            game.board.set_piece(to_x, to_y, captured_piece)
            game.current_player = old_current_player
            game.game_over = old_game_over
            game.winner = old_winner
            
            if score > best_score:
                best_score = score
                best_move = (from_x, from_y, to_x, to_y)
        
        return best_move
    
    def _minimax(self, game: 'ChessGame', depth: int, is_maximizing: bool, ai_color: Color) -> float:
        """Algoritmo Minimax com profundidade limitada"""
        # Avaliar posição terminal
        if depth == 0 or game.game_over:
            return self._evaluate_board(game, ai_color)
        
        opponent_color = Color.BLACK if ai_color == Color.WHITE else Color.WHITE
        current_color = ai_color if is_maximizing else opponent_color
        
        # Coletar todos os movimentos possíveis para a cor atual
        all_moves = []
        for y in range(8):
            for x in range(8):
                piece = game.board.get_piece(x, y)
                if piece and piece.color == current_color:
                    moves = game.get_piece_moves(x, y)
                    for to_x, to_y in moves:
                        all_moves.append((x, y, to_x, to_y))
        
        if not all_moves:
            # Sem movimentos: xeque-mate ou afogamento
            if game.is_in_check(current_color):
                return float('-inf') if is_maximizing else float('inf')
            else:
                return 0
        
        if is_maximizing:
            max_eval = float('-inf')
            for from_x, from_y, to_x, to_y in all_moves:
                # Salvar estado
                captured_piece = game.board.get_piece(to_x, to_y)
                piece = game.board.get_piece(from_x, from_y)
                old_current_player = game.current_player
                
                # Executar movimento
                game.board.set_piece(to_x, to_y, piece)
                game.board.set_piece(from_x, from_y, None)
                game.current_player = opponent_color
                
                eval_score = self._minimax(game, depth - 1, False, ai_color)
                
                # Restaurar estado
                game.board.set_piece(from_x, from_y, piece)
                game.board.set_piece(to_x, to_y, captured_piece)
                game.current_player = old_current_player
                
                max_eval = max(max_eval, eval_score)
            
            return max_eval
        else:
            min_eval = float('inf')
            for from_x, from_y, to_x, to_y in all_moves:
                # Salvar estado
                captured_piece = game.board.get_piece(to_x, to_y)
                piece = game.board.get_piece(from_x, from_y)
                old_current_player = game.current_player
                
                # Executar movimento
                game.board.set_piece(to_x, to_y, piece)
                game.board.set_piece(from_x, from_y, None)
                game.current_player = ai_color
                
                eval_score = self._minimax(game, depth - 1, True, ai_color)
                
                # Restaurar estado
                game.board.set_piece(from_x, from_y, piece)
                game.board.set_piece(to_x, to_y, captured_piece)
                game.current_player = old_current_player
                
                min_eval = min(min_eval, eval_score)
            
            return min_eval
    
    def _evaluate_board(self, game: 'ChessGame', ai_color: Color) -> float:
        """Avalia a qualidade da posição atual"""
        score = 0.0
        opponent_color = Color.BLACK if ai_color == Color.WHITE else Color.WHITE
        
        # Verificar xeque-mate primeiro (máxima prioridade)
        if game.game_over and game.winner == ai_color:
            return float('inf')
        if game.game_over and game.winner == opponent_color:
            return float('-inf')
        
        # Contar material (valor das peças)
        for y in range(8):
            for x in range(8):
                piece = game.board.get_piece(x, y)
                if piece:
                    piece_value = self.PIECE_VALUES.get(piece.piece_type, 0)
                    if piece.color == ai_color:
                        score += piece_value
                    else:
                        score -= piece_value
        
        # Bônus por posição dos peões (peões avançados são mais valiosos)
        for y in range(8):
            for x in range(8):
                piece = game.board.get_piece(x, y)
                if piece and piece.piece_type == PieceType.PAWN:
                    if piece.color == ai_color:
                        # Peões brancos mais perto da fileira 8 são melhores
                        if ai_color == Color.WHITE:
                            advance = 7 - y
                            score += advance * 0.3
                        else:
                            advance = y
                            score += advance * 0.3
                    else:
                        if opponent_color == Color.WHITE:
                            advance = 7 - y
                            score -= advance * 0.3
                        else:
                            advance = y
                            score -= advance * 0.3
        
        # Bônus por controlar o centro
        center_squares = [(3, 3), (3, 4), (4, 3), (4, 4)]
        for cx, cy in center_squares:
            piece = game.board.get_piece(cx, cy)
            if piece:
                if piece.color == ai_color:
                    score += 0.2
                else:
                    score -= 0.2
        
        # Verificar se o rei está em perigo
        king_pos = game.board.find_king(ai_color)
        if king_pos and game.is_under_attack(king_pos[0], king_pos[1], opponent_color):
            score -= 40  # Grande penalidade se está em xeque
        
        # Bônus se o rei inimigo está em perigo
        opponent_king_pos = game.board.find_king(opponent_color)
        if opponent_king_pos and game.is_under_attack(opponent_king_pos[0], opponent_king_pos[1], ai_color):
            score += 40  # Grande bônus se pode atacar o rei inimigo
        
        return score

def main(difficulty: str = 'medium', player_color: str = 'white'):
    """
    Inicia o jogo de xadrez contra a IA
    
    Args:
        difficulty: 'easy', 'medium' ou 'hard'
        player_color: 'white' ou 'black'
    """
    player_color_enum = Color.WHITE if player_color.lower() == 'white' else Color.BLACK
    game = ChessGame(
        ai_enabled=True,
        ai_difficulty=difficulty,
        player_color=player_color_enum
    )
    game.run()

if __name__ == '__main__':
    main()
