import os
import pygame as pg


class Chess:
    def __init__(self):
        pg.init()
        self.base_dir = os.path.dirname(os.path.abspath(__file__))
        self.green        = (115, 150,  80)
        self.green_light  = (235, 235, 210)
        self.black_alpha  = (  0,   0,   0,  50)

        self.window = pg.display.set_mode((800, 800))
        pg.display.set_caption('Xadrez')

        pg.font.init()
        self.font = pg.font.SysFont("Courier New", 25, bold=True)

        self.clock = pg.time.Clock()

        # Mouse variables
        self.last_click_status = (False, False, False)

        # Game state flags
        self.game_over = False
        self.in_check = False
        self.winner = None
        self.game_result = ''
        self.prev_in_check = False

        # Move history / undo
        self.move_history = []          # list of move strings
        self.state_history = []         # list of board snapshots for undo

        # Sounds (optional). Put wav files in Xadrez/sounds: move.wav, check.wav, mate.wav
        self.sounds = {'move': None, 'check': None, 'mate': None}
        try:
            pg.mixer.init()
            for name, fname in [('move', 'move.wav'), ('check', 'check.wav'), ('mate', 'mate.wav')]:
                path = os.path.join(self.base_dir, 'sounds', fname)
                if os.path.exists(path):
                    self.sounds[name] = pg.mixer.Sound(path)
        except Exception:
            # sound support not available; continue without sounds
            self.sounds = {'move': None, 'check': None, 'mate': None}

        self.player_view = 'white'
        self.player_turn = 'white'
        self.selected_piece = None
        self.last_selected_piece = None
        self.click_position = None
        self.last_click_position = None
        self.en_passant = None
        self.white_castling_movement_condition = [True, True, True]
        self.black_castling_movement_condition = [True, True, True]

        self.board_map = [['b_rk','b_kn','b_bs','b_qn','b_kg','b_bs','b_kn','b_rk'],
                          ['b_pw','b_pw','b_pw','b_pw','b_pw','b_pw','b_pw','b_pw'],
                          [    '',    '',    '',    '',    '',    '',    '',    ''],
                          [    '',    '',    '',    '',    '',    '',    '',    ''],
                          [    '',    '',    '',    '',    '',    '',    '',    ''],
                          [    '',    '',    '',    '',    '',    '',    '',    ''],
                          ['w_pw','w_pw','w_pw','w_pw','w_pw','w_pw','w_pw','w_pw'],
                          ['w_rk','w_kn','w_bs','w_qn','w_kg','w_bs','w_kn','w_rk']]

        self.actions_board_map = [['','','','','','','',''],
                                  ['','','','','','','',''],
                                  ['','','','','','','',''],
                                  ['','','','','','','',''],
                                  ['','','','','','','',''],
                                  ['','','','','','','',''],
                                  ['','','','','','','',''],
                                  ['','','','','','','','']]

        black_pawn   = pg.image.load(os.path.join(self.base_dir, 'pawn black.png'))
        black_knight = pg.image.load(os.path.join(self.base_dir, 'knight black.png'))
        black_bishop = pg.image.load(os.path.join(self.base_dir, 'bishop black.png'))
        black_rook   = pg.image.load(os.path.join(self.base_dir, 'rook black.png'))
        black_queen  = pg.image.load(os.path.join(self.base_dir, 'queen black.png'))
        black_king   = pg.image.load(os.path.join(self.base_dir, 'king black.png'))
        white_pawn   = pg.image.load(os.path.join(self.base_dir, 'pawn white.png'))
        white_knight = pg.image.load(os.path.join(self.base_dir, 'knight white.png'))
        white_bishop = pg.image.load(os.path.join(self.base_dir, 'bishop white.png'))
        white_rook   = pg.image.load(os.path.join(self.base_dir, 'rook white.png'))
        white_queen  = pg.image.load(os.path.join(self.base_dir, 'queen white.png'))
        white_king   = pg.image.load(os.path.join(self.base_dir, 'king white.png'))
        self.black_pawn   = pg.transform.scale(black_pawn  , (100, 100))
        self.black_knight = pg.transform.scale(black_knight, (100, 100))
        self.black_bishop = pg.transform.scale(black_bishop, (100, 100))
        self.black_rook   = pg.transform.scale(black_rook  , (100, 100))
        self.black_queen  = pg.transform.scale(black_queen , (100, 100))
        self.black_king   = pg.transform.scale(black_king  , (100, 100))
        self.white_pawn   = pg.transform.scale(white_pawn  , (100, 100))
        self.white_knight = pg.transform.scale(white_knight, (100, 100))
        self.white_bishop = pg.transform.scale(white_bishop, (100, 100))
        self.white_rook   = pg.transform.scale(white_rook  , (100, 100))
        self.white_queen  = pg.transform.scale(white_queen , (100, 100))
        self.white_king   = pg.transform.scale(white_king  , (100, 100))

    def mouse_has_clicked(self, input):
            if self.last_click_status == input:
                return (False, False, False)
            else:
                left_button = False
                center_button = False
                right_button = False
                if self.last_click_status[0] == False and input[0] == True:
                    left_button = True
                if self.last_click_status[1] == False and input[1] == True:
                    center_button = True
                if self.last_click_status[2] == False and input[2] == True:
                    right_button = True

                return (left_button, center_button, right_button)

    def position_board_pieces(self):
        for y in range(8):
            for x in range(8):
                if self.board_map[y][x] == 'b_pw':
                    self.window.blit(self.black_pawn, (x*100, y*100))
                elif self.board_map[y][x] == 'b_rk':
                    self.window.blit(self.black_rook, (x*100, y*100))
                elif self.board_map[y][x] == 'b_kn':
                    self.window.blit(self.black_knight, (x*100, y*100))
                elif self.board_map[y][x] == 'b_bs':
                    self.window.blit(self.black_bishop, (x*100, y*100))
                elif self.board_map[y][x] == 'b_qn':
                    self.window.blit(self.black_queen, (x*100, y*100))
                elif self.board_map[y][x] == 'b_kg':
                    self.window.blit(self.black_king, (x*100, y*100))
                elif self.board_map[y][x] == 'w_pw':
                    self.window.blit(self.white_pawn, (x*100, y*100))
                elif self.board_map[y][x] == 'w_rk':
                    self.window.blit(self.white_rook, (x*100, y*100))
                elif self.board_map[y][x] == 'w_kn':
                    self.window.blit(self.white_knight, (x*100, y*100))
                elif self.board_map[y][x] == 'w_bs':
                    self.window.blit(self.white_bishop, (x*100, y*100))
                elif self.board_map[y][x] == 'w_qn':
                    self.window.blit(self.white_queen, (x*100, y*100))
                elif self.board_map[y][x] == 'w_kg':
                    self.window.blit(self.white_king, (x*100, y*100))

    def draw_pieces_next_moves(self):
        circle_surf = pg.Surface((100, 100), pg.SRCALPHA)
        pg.draw.circle(circle_surf, self.black_alpha, (50, 50), 50, 10)

        dot_surf = pg.Surface((100, 100), pg.SRCALPHA)
        pg.draw.circle(dot_surf, self.black_alpha, (50, 50), 15)

        for y in range(8):
            for x in range(8):
                if self.actions_board_map[y][x] == 'o':
                    self.window.blit(circle_surf, (x*100, y*100))
                elif self.actions_board_map[y][x] == '.':
                    self.window.blit(dot_surf, (x*100, y*100))

    def board(self):
        columns = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
        for y in range(8):
            for x in range(8):
                if (y % 2) == 0 and (x % 2) == 0 or (y % 2) != 0 and (x % 2) != 0:
                        pg.draw.rect(self.window, self.green_light, (x * 100, y * 100, 100, 100))
                elif (y % 2) != 0 and (x % 2) == 0 or (y % 2) == 0 and (x % 2) != 0:
                        pg.draw.rect(self.window, self.green, ((x * 100, y * 100, 100, 100)))
                if x == 0 and y % 2 == 0:
                    if self.player_view == 'white':
                        score_text = self.font.render(str(8-y), 1, self.green)
                        self.window.blit(score_text, (5, (y * 100) + 5))
                    else:
                        score_text = self.font.render(str(y+1), 1, self.green)
                        self.window.blit(score_text, (5, (y * 100) + 5))
                elif x == 0 and y % 2 == 1:
                    if self.player_view == 'white':
                        score_text = self.font.render(str(8-y), 1, self.green_light)
                        self.window.blit(score_text, (5, (y * 100) + 5))
                    else:
                        score_text = self.font.render(str(y+1), 1, self.green_light)
                        self.window.blit(score_text, (5, (y * 100) + 5))
                if y == 7 and x % 2 == 1:
                    if self.player_view == 'white':
                        score_text = self.font.render(columns[x], 1, self.green)
                        self.window.blit(score_text, ((x * 100) + 80, 775))
                    else:
                        score_text = self.font.render(columns[7-x], 1, self.green)
                        self.window.blit(score_text, ((x * 100) + 80, 775))
                elif y == 7 and x % 2 == 0:
                    if self.player_view == 'white':
                        score_text = self.font.render(columns[x], 1, self.green_light)
                        self.window.blit(score_text, ((x * 100) + 80, 775))
                    else:
                        score_text = self.font.render(columns[7-x], 1, self.green_light)
                        self.window.blit(score_text, ((x * 100) + 80, 775))

        self.position_board_pieces()

        self.draw_pieces_next_moves()

        # Status: check / checkmate / stalemate (PT-BR)
        if getattr(self, 'game_over', False):
            status_text = self.font.render(self.game_result, 1, self.green)
            self.window.blit(status_text, (10, 10))
        else:
            if getattr(self, 'in_check', False):
                name = 'Branco' if self.player_turn == 'white' else 'Preto'
                status = f"Xeque — {name}"
                status_text = self.font.render(status, 1, self.green)
                self.window.blit(status_text, (10, 10))

    def pawn_promotion(self):
        x = self.click_position[0]
        y = self.click_position[1]
        if self.board_map[y][x] == 'w_pw':
            if self.player_view == 'white' and y == 0:
                self.board_map[y][x] = 'w_qn'
            if self.player_view == 'black' and y == 7:
                self.board_map[y][x] = 'w_qn'
        elif self.board_map[y][x] == 'b_pw':
            if self.player_view == 'white' and y == 7:
                self.board_map[y][x] = 'b_qn'
            if self.player_view == 'black' and y == 0:
                self.board_map[y][x] = 'b_qn'

    def en_passant_move(self):
        x = self.click_position[0]
        y = self.click_position[1]
        last_y = self.last_click_position[1]
        if self.selected_piece[2:5] == 'pw':
            if y == 3 and last_y == 1:
                self.en_passant = [x, last_y+1]
            elif y == 4 and last_y == 6:
                self.en_passant = [x, last_y-1]

    def castling(self):
        x = self.click_position[0]
        y = self.click_position[1]
        last_x = self.last_click_position[0]
        last_y = self.last_click_position[1]
        last_selected_piece = self.board_map[last_y][last_x]
        if self.player_view == 'white' and self.player_turn == 'white' and last_selected_piece == 'w_kg':
            if x == 6 and y == 7 and last_x == 4 and last_y == 7:
                self.board_map[7][7] = ''
                self.board_map[7][5] = 'w_rk'
                self.white_castling_movement_condition[2] = False
                self.white_castling_movement_condition[1] = False
            elif x == 2 and y == 7 and last_x == 4 and last_y == 7:
                self.board_map[7][0] = ''
                self.board_map[7][3] = 'w_rk'
                self.white_castling_movement_condition[0] = False
                self.white_castling_movement_condition[1] = False
        elif self.player_view == 'white' and self.player_turn == 'black' and last_selected_piece == 'b_kg':
            if x == 6 and y == 0  and last_x == 4 and last_y == 0:
                self.board_map[0][7] = ''
                self.board_map[0][5] = 'b_rk'
                self.black_castling_movement_condition[2] = False
                self.black_castling_movement_condition[1] = False
            elif x == 2 and y == 0 and last_x == 4 and last_y == 0:
                self.board_map[0][0] = ''
                self.board_map[0][3] = 'b_rk'
                self.black_castling_movement_condition[0] = False
                self.black_castling_movement_condition[1] = False
        elif self.player_view == 'black' and self.player_turn == 'white' and last_selected_piece == 'w_kg':
            if x == 5 and y == 0 and last_x == 3 and last_y == 0:
                self.board_map[0][7] = ''
                self.board_map[0][4] = 'w_rk'
                self.white_castling_movement_condition[2] = False
                self.white_castling_movement_condition[1] = False
            elif x == 1 and y == 0 and last_x == 3 and last_y == 0:
                self.board_map[0][0] = ''
                self.board_map[0][2] = 'w_rk'
                self.white_castling_movement_condition[0] = False
                self.white_castling_movement_condition[1] = False
        elif self.player_view == 'black' and self.player_turn == 'black' and last_selected_piece == 'b_kg':
            if x == 5 and y == 7 and last_x == 3 and last_y == 7:
                self.board_map[7][7] = ''
                self.board_map[7][4] = 'b_rk'
                self.black_castling_movement_condition[2] = False
                self.black_castling_movement_condition[1] = False
            elif x == 1 and y == 7 and last_x == 3 and last_y == 7:
                self.board_map[7][0] = ''
                self.board_map[7][2] = 'b_rk'
                self.black_castling_movement_condition[0] = False
                self.black_castling_movement_condition[1] = False

    def castling_path(self):
        x = self.click_position[0]
        y = self.click_position[1]
        last_selected_piece = self.board_map[y][x]
        if self.player_view == 'white' and self.player_turn == 'white' and last_selected_piece == 'w_kg':
            if self.white_castling_movement_condition[1]:
                if self.white_castling_movement_condition[0]:
                    if self.board_map[7][3] == '' and self.board_map[7][2] == '' and self.board_map[7][1] == '':
                        if self.is_king_in_check('b', 4, 7) == False and self.is_king_in_check('b', 3, 7) == False and self.is_king_in_check('b', 2, 7) == False:
                            self.actions_board_map[7][2] = '.'
                if self.white_castling_movement_condition[2]:
                    if self.board_map[7][5] == '' and self.board_map[7][6] == '':
                        if self.is_king_in_check('b', 4, 7) == False and self.is_king_in_check('b', 5, 7) == False and self.is_king_in_check('b', 6, 7) == False:
                            self.actions_board_map[7][6] = '.'
        elif self.player_view == 'white' and self.player_turn == 'black' and last_selected_piece == 'b_kg':
            if self.black_castling_movement_condition[1]:
                if self.black_castling_movement_condition[0]:
                    if self.board_map[0][3] == '' and self.board_map[0][2] == '' and self.board_map[0][1] == '':
                        if self.is_king_in_check('w', 4, 0) == False and self.is_king_in_check('w', 3, 0) == False and self.is_king_in_check('w', 2, 0) == False:
                            self.actions_board_map[0][2] = '.'
                if self.black_castling_movement_condition[2]:
                    if self.board_map[0][5] == '' and self.board_map[0][6] == '':
                        if self.is_king_in_check('w', 4, 0) == False and self.is_king_in_check('w', 5, 0) == False and self.is_king_in_check('w', 6, 0) == False:
                            self.actions_board_map[0][6] = '.'
        elif self.player_view == 'black' and self.player_turn == 'white' and last_selected_piece == 'w_kg':
            if self.white_castling_movement_condition[1]:
                if self.white_castling_movement_condition[0]:
                    if self.board_map[0][2] == '' and self.board_map[0][1] == '':
                        if self.is_king_in_check('b', 3, 0) == False and self.is_king_in_check('b', 2, 0) == False and self.is_king_in_check('b', 1, 0) == False:
                            self.actions_board_map[0][1] = '.'
                if self.white_castling_movement_condition[2]:
                    if self.board_map[0][4] == '' and self.board_map[0][5] == '' and self.board_map[0][6] == '':
                        if self.is_king_in_check('b', 3, 0) == False and self.is_king_in_check('b', 4, 0) == False and self.is_king_in_check('b', 5, 0) == False:
                            self.actions_board_map[0][5] = '.'
        elif self.player_view == 'black' and self.player_turn == 'black' and last_selected_piece == 'b_kg':
            if self.black_castling_movement_condition[1]:
                if self.black_castling_movement_condition[0]:
                    if self.board_map[7][2] == '' and self.board_map[7][1] == '':
                        if self.is_king_in_check('w', 3, 7) == False and self.is_king_in_check('w', 2, 7) == False and self.is_king_in_check('w', 1, 7) == False:
                            self.actions_board_map[7][1] = '.'
                if self.black_castling_movement_condition[2]:
                    if self.board_map[7][4] == '' and self.board_map[7][5] == '' and self.board_map[7][6] == '':
                        if self.is_king_in_check('w', 3, 7) == False and self.is_king_in_check('w', 4, 7) == False and self.is_king_in_check('w', 5, 7) == False:
                            self.actions_board_map[7][5] = '.'

    def castling_variables_update(self):
        x = self.click_position[0]
        y = self.click_position[1]
        last_x = self.last_click_position[0]
        last_y = self.last_click_position[1]
        moved_piece = self.board_map[last_y][last_x]
        if moved_piece[2:5] in ['rk', 'kg']:
            if self.player_view == 'white' and self.player_turn == 'white':
                if self.white_castling_movement_condition[0] == True and last_x == 0 and last_y == 7:
                    self.white_castling_movement_condition[0] = False
                elif self.white_castling_movement_condition[1] == True and last_x == 4 and last_y == 7:
                    if x >= 3 and y >= 6 and x <= 5:
                        self.white_castling_movement_condition[1] = False
                elif self.white_castling_movement_condition[2] == True and last_x == 7 and last_y == 7:
                    self.white_castling_movement_condition[2] = False
            elif self.player_view == 'white' and self.player_turn == 'black':
                if self.black_castling_movement_condition[0] == True and last_x == 0 and last_y == 0:
                    self.black_castling_movement_condition[0] = False
                elif self.black_castling_movement_condition[1] == True and last_x == 4 and last_y == 0:
                    if x >= 3 and y <= 1 and x <= 5:
                        self.black_castling_movement_condition[1] = False
                elif self.black_castling_movement_condition[2] == True and last_x == 7 and last_y == 0:
                    self.black_castling_movement_condition[2] = False
            elif self.player_view == 'black' and self.player_turn == 'white':
                if self.white_castling_movement_condition[0] == True and last_x == 0 and last_y == 0:
                    self.white_castling_movement_condition[0] = False
                elif self.white_castling_movement_condition[1] == True and last_x == 3 and last_y == 0:
                    if x >= 2 and y >= 1 and x <= 4:
                        self.white_castling_movement_condition[1] = False
                elif self.white_castling_movement_condition[2] == True and last_x == 7 and last_y == 0:
                    self.white_castling_movement_condition[2] = False
            elif self.player_view == 'black' and self.player_turn == 'black':
                if self.black_castling_movement_condition[0] == True and last_x == 0 and last_y == 7:
                    self.black_castling_movement_condition[0] = False
                elif self.black_castling_movement_condition[1] == True and last_x == 3 and last_y == 7:
                    if x >= 2 and y <= 6 and x <= 4:
                        self.black_castling_movement_condition[1] = False
                elif self.black_castling_movement_condition[2] == True and last_x == 7 and last_y == 7:
                    self.black_castling_movement_condition[2] = False

    def piece_move_or_capture(self):
        # Do not allow moves after game over
        if getattr(self, 'game_over', False):
            return

        if self.selected_piece != None and self.last_click_position != None:
            x = self.click_position[0]
            y = self.click_position[1]
            last_x = self.last_click_position[0]
            last_y = self.last_click_position[1]
            moved_piece = self.board_map[last_y][last_x]
            # Move or capture
            if self.actions_board_map[y][x] == '.' or self.actions_board_map[y][x] == 'o':
                # save snapshot for undo
                snapshot = {
                    'board_map': [row[:] for row in self.board_map],
                    'player_turn': self.player_turn,
                    'en_passant': None if self.en_passant is None else list(self.en_passant),
                    'white_castling_movement_condition': list(self.white_castling_movement_condition),
                    'black_castling_movement_condition': list(self.black_castling_movement_condition)
                }
                self.state_history.append(snapshot)

                # compute move notation
                def coord_to_alg(xx, yy):
                    return chr(ord('a') + xx) + str(8 - yy)
                move_notation = coord_to_alg(last_x, last_y) + '->' + coord_to_alg(x, y)

                # Castling variables update
                self.castling_variables_update()
                # Castling Rook move
                self.castling()
                # Moving pieces
                self.board_map[y][x] = moved_piece
                self.selected_piece = moved_piece
                self.board_map[last_y][last_x] = ''
                # En Passant capture
                if moved_piece[2:5] == 'pw':
                    if self.en_passant != None:
                        x_ep = self.en_passant[0]
                        y_ep = self.en_passant[1]
                        if x_ep == x and y_ep == y:
                            if last_y > y:
                                self.board_map[y+1][x] = ''
                            elif last_y < y:
                                self.board_map[y-1][x] = ''
                self.pawn_promotion()

                # record move in history
                self.move_history.append(move_notation)
                # play move sound if available
                if self.sounds.get('move'):
                    try:
                        self.sounds['move'].play()
                    except Exception:
                        pass

                if self.player_turn == 'white':
                    self.player_turn = 'black'
                    self.en_passant = None
                elif self.player_turn == 'black':
                    self.player_turn = 'white'
                    self.en_passant = None
                self.en_passant_move()

                # Update check / mate state and play sounds as needed
                self.update_check_and_game_state()
                if getattr(self, 'in_check', False) and not getattr(self, 'prev_in_check', False):
                    if self.sounds.get('check'):
                        try:
                            self.sounds['check'].play()
                        except Exception:
                            pass
                self.prev_in_check = getattr(self, 'in_check', False)
                if getattr(self, 'game_over', False):
                    if self.sounds.get('mate'):
                        try:
                            self.sounds['mate'].play()
                        except Exception:
                            pass

    # ---- Move validation & game state detection ----
    def find_king(self, color_char):
        king = color_char + '_kg'
        for y in range(8):
            for x in range(8):
                if self.board_map[y][x] == king:
                    return (x, y)
        return None

    def _move_leaves_king_in_check(self, from_x, from_y, to_x, to_y):
        # Simulate the move and determine if own king would be in check
        tmp = [row[:] for row in self.board_map]
        moved_piece = tmp[from_y][from_x]
        if moved_piece == '':
            return True
        # apply move
        tmp[to_y][to_x] = moved_piece
        tmp[from_y][from_x] = ''
        # handle en passant capture
        if moved_piece[2:5] == 'pw' and self.en_passant is not None and [to_x, to_y] == self.en_passant:
            if from_y > to_y:
                tmp[to_y+1][to_x] = ''
            else:
                tmp[to_y-1][to_x] = ''
        # handle castling rook movement if king moved two squares
        if moved_piece[2:5] == 'kg' and abs(to_x - from_x) == 2:
            row = from_y
            if to_x > from_x:
                # kingside
                tmp[row][5] = tmp[row][7]
                tmp[row][7] = ''
            else:
                # queenside
                tmp[row][3] = tmp[row][0]
                tmp[row][0] = ''
        # find king position for the moved color
        color = moved_piece[0:1]
        king_name = color + '_kg'
        king_pos = None
        for yy in range(8):
            for xx in range(8):
                if tmp[yy][xx] == king_name:
                    king_pos = (xx, yy)
                    break
            if king_pos:
                break
        if not king_pos:
            return True
        # Temporarily swap board and call check routine
        original_board = self.board_map
        self.board_map = tmp
        try:
            in_check = self.is_king_in_check('b' if color == 'w' else 'w', king_pos[0], king_pos[1])
        finally:
            self.board_map = original_board
        return in_check

    def filter_moves_for_selected(self):
        if self.selected_piece is None or self.click_position is None:
            return
        from_x = self.click_position[0]
        from_y = self.click_position[1]
        for y in range(8):
            for x in range(8):
                if self.actions_board_map[y][x] in ['.', 'o']:
                    if self._move_leaves_king_in_check(from_x, from_y, x, y):
                        self.actions_board_map[y][x] = ''

    def player_has_any_legal_moves(self, color_char):
        # Iterate all pieces of color_char and check if any legal move exists
        saved_selected = self.selected_piece
        saved_click = self.click_position
        for y in range(8):
            for x in range(8):
                piece = self.board_map[y][x]
                if piece != '' and piece[0:1] == color_char:
                    self.selected_piece = piece
                    self.click_position = [x, y]
                    self.clear_map_actions()
                    typ = piece[2:5]
                    if typ == 'pw':
                        self.pawn_move()
                    elif typ == 'kn':
                        self.knight_move()
                    elif typ == 'bs':
                        self.bishop_move()
                    elif typ == 'rk':
                        self.rook_move()
                    elif typ == 'qn':
                        self.queen_move()
                    elif typ == 'kg':
                        self.king_move()
                    self.filter_moves_for_selected()
                    # if any legal move exists
                    for yy in range(8):
                        for xx in range(8):
                            if self.actions_board_map[yy][xx] in ['.', 'o']:
                                # restore
                                self.selected_piece = saved_selected
                                self.click_position = saved_click
                                self.clear_map_actions()
                                return True
        # restore
        self.selected_piece = saved_selected
        self.click_position = saved_click
        self.clear_map_actions()
        return False

    def update_check_and_game_state(self):
        # Determine if current player (self.player_turn) is in check and whether no legal moves => checkmate/stalemate
        current_char = 'w' if self.player_turn == 'white' else 'b'
        opponent_char = 'b' if current_char == 'w' else 'w'
        king_pos = self.find_king(current_char)
        if king_pos is None:
            return
        in_check = self.is_king_in_check(opponent_char, king_pos[0], king_pos[1])
        self.in_check = in_check
        any_moves = self.player_has_any_legal_moves(current_char)
        if not any_moves:
            self.game_over = True
            if in_check:
                # checkmate — opponent wins (PT-BR)
                winner = 'Branco' if opponent_char == 'w' else 'Preto'
                self.winner = winner
                self.game_result = f'Xeque-mate — {self.winner} venceu'
            else:
                self.winner = None
                self.game_result = 'Empate — afogamento'
        else:
            self.game_over = False
            self.winner = None
            self.game_result = ''
        # Play check sound if entering check
        if self.in_check and not getattr(self, 'prev_in_check', False):
            if self.sounds.get('check'):
                try:
                    self.sounds['check'].play()
                except Exception:
                    pass
        self.prev_in_check = self.in_check

    def piece_path(self, path, opposing_piece, step_x, step_y):
        x = self.click_position[0]
        y = self.click_position[1]
        if x + step_x <= -1 or y + step_y <= -1:
            return False
        try:
            if path == True:
                if self.board_map[y+step_y][x+step_x] == '':
                    self.actions_board_map[y+step_y][x+step_x] = '.'
                    return True
                elif self.board_map[y+step_y][x+step_x][0:1] == opposing_piece:
                    self.actions_board_map[y+step_y][x+step_x] = 'o'
                    return False
            else:
                return False
        except:
            return False

    def undo_move(self):
        if not self.state_history:
            return
        snapshot = self.state_history.pop()
        self.board_map = [row[:] for row in snapshot['board_map']]
        self.player_turn = snapshot['player_turn']
        self.en_passant = None if snapshot['en_passant'] is None else list(snapshot['en_passant'])
        self.white_castling_movement_condition = list(snapshot['white_castling_movement_condition'])
        self.black_castling_movement_condition = list(snapshot['black_castling_movement_condition'])
        if self.move_history:
            self.move_history.pop()
        self.game_over = False
        self.in_check = False
        self.winner = None
        self.game_result = ''
        self.prev_in_check = False

    def clear_map_actions(self):
        # Clear self.actions_board_map
        for y in range(8):
            for x in range(8):
                self.actions_board_map[y][x] = ''

    def pawn_move(self):
        # Pawn next moves
        if self.selected_piece != None:
            if self.selected_piece[2:5] == 'pw':
                x = self.click_position[0]
                y = self.click_position[1]
                if self.player_view == 'white' and self.player_turn == 'white' and self.selected_piece[0:1] == 'w':
                    if y >= 1:
                        if self.board_map[y-1][x-1][0:1] == 'b':
                            self.actions_board_map[y-1][x-1] = 'o'
                        if self.board_map[y-1][x] == '':
                            self.actions_board_map[y-1][x] = '.'
                            if y == 6 and self.board_map[y-2][x] == '':
                                self.actions_board_map[y-2][x] = '.'
                        if x < 7 and self.board_map[y-1][x+1][0:1] == 'b':
                            self.actions_board_map[y-1][x+1] = 'o'
                        if self.en_passant != None:
                            x_ep = self.en_passant[0]
                            y_ep = self.en_passant[1]
                            if y_ep == y-1 and x_ep == x-1:
                                self.actions_board_map[y-1][x-1] = 'o'
                            elif y_ep == y-1 and x_ep == x+1:
                                self.actions_board_map[y-1][x+1] = 'o'
                if self.player_view == 'white' and self.player_turn == 'black' and self.selected_piece[0:1] == 'b':
                    if y <= 6:
                        if self.board_map[y+1][x-1][0:1] == 'w':
                            self.actions_board_map[y+1][x-1] = 'o'
                        if self.board_map[y+1][x] == '':
                            self.actions_board_map[y+1][x] = '.'
                            if y == 1 and self.board_map[y+2][x] == '':
                                self.actions_board_map[y+2][x] = '.'
                        if x < 7 and self.board_map[y+1][x+1][0:1] == 'w':
                            self.actions_board_map[y+1][x+1] = 'o'
                        if self.en_passant != None:
                            x_ep = self.en_passant[0]
                            y_ep = self.en_passant[1]
                            if y_ep == y+1 and x_ep == x-1:
                                self.actions_board_map[y+1][x-1] = 'o'
                            elif y_ep == y+1 and x_ep == x+1:
                                self.actions_board_map[y+1][x+1] = 'o'
                if self.player_view == 'black' and self.player_turn == 'black' and self.selected_piece[0:1] == 'b':
                    if y >= 1:
                        if self.board_map[y-1][x-1][0:1] == 'w':
                            self.actions_board_map[y-1][x-1] = 'o'
                        if self.board_map[y-1][x] == '':
                            self.actions_board_map[y-1][x] = '.'
                            if y == 6 and self.board_map[y-2][x] == '':
                                self.actions_board_map[y-2][x] = '.'
                        if x < 7 and self.board_map[y-1][x+1][0:1] == 'w':
                            self.actions_board_map[y-1][x+1] = 'o'
                        if self.en_passant != None:
                            x_ep = self.en_passant[0]
                            y_ep = self.en_passant[1]
                            if y_ep == y-1 and x_ep == x-1:
                                self.actions_board_map[y-1][x-1] = 'o'
                            elif y_ep == y-1 and x_ep == x+1:
                                self.actions_board_map[y-1][x+1] = 'o'
                if self.player_view == 'black' and self.player_turn == 'white' and self.selected_piece[0:1] == 'w':
                    if y <= 6:
                        if self.board_map[y+1][x-1][0:1] == 'b':
                            self.actions_board_map[y+1][x-1] = 'o'
                        if self.board_map[y+1][x] == '':
                            self.actions_board_map[y+1][x] = '.'
                            if y == 1 and self.board_map[y+2][x] == '':
                                self.actions_board_map[y+2][x] = '.'
                        if x < 7 and self.board_map[y+1][x+1][0:1] == 'b':
                            self.actions_board_map[y+1][x+1] = 'o'
                        if self.en_passant != None:
                            x_ep = self.en_passant[0]
                            y_ep = self.en_passant[1]
                            if y_ep == y+1 and x_ep == x-1:
                                self.actions_board_map[y+1][x-1] = 'o'
                            elif y_ep == y+1 and x_ep == x+1:
                                self.actions_board_map[y+1][x+1] = 'o'

    def knight_move(self):
        # Knight next moves
        if self.selected_piece != None:
            if self.selected_piece[2:5] == 'kn':
                x = self.click_position[0]
                y = self.click_position[1]
                direction = True
                moves = [[1, 2], [2, 1], [2, -1], [1, -2], [-1, -2], [-2, -1], [-2, 1], [-1 , 2]]
                for move in moves:
                    # Up + Right
                    if self.player_turn == 'white' and self.board_map[y][x][0:1] == 'w':
                        _ = self.piece_path(direction, 'b', move[0], move[1])
                    elif self.player_turn == 'black' and self.board_map[y][x][0:1] == 'b':
                        _ = self.piece_path(direction, 'w', move[0], move[1])

    def bishop_move(self):
        # Bishop next moves
        if self.selected_piece != None:
            if self.selected_piece[2:5] == 'bs':
                x = self.click_position[0]
                y = self.click_position[1]
                direction = [True, True, True, True]
                for move in range(1, 8):
                    # Up + Right
                    if self.player_turn == 'white' and self.board_map[y][x][0:1] == 'w':
                        direction[0] = self.piece_path(direction[0], 'b', move, -move)
                    elif self.player_turn == 'black' and self.board_map[y][x][0:1] == 'b':
                        direction[0] = self.piece_path(direction[0], 'w', move, -move)
                    # Down + Right
                    if self.player_turn == 'white' and self.board_map[y][x][0:1] == 'w':
                        direction[1] = self.piece_path(direction[1], 'b', move, move)
                    elif self.player_turn == 'black' and self.board_map[y][x][0:1] == 'b':
                        direction[1] = self.piece_path(direction[1], 'w', move, move)
                    # Down + Left
                    if self.player_turn == 'white' and self.board_map[y][x][0:1] == 'w':
                        direction[2] = self.piece_path(direction[2], 'b', -move, move)
                    elif self.player_turn == 'black' and self.board_map[y][x][0:1] == 'b':
                        direction[2] = self.piece_path(direction[2], 'w', -move, move)
                    # Up + Left
                    if self.player_turn == 'white' and self.board_map[y][x][0:1] == 'w':
                        direction[3] = self.piece_path(direction[3], 'b', -move, -move)
                    elif self.player_turn == 'black' and self.board_map[y][x][0:1] == 'b':
                        direction[3] = self.piece_path(direction[3], 'w', -move, -move)

    def rook_move(self):
        # Rook next moves
        if self.selected_piece != None:
            if self.selected_piece[2:5] == 'rk':
                x = self.click_position[0]
                y = self.click_position[1]
                direction = [True, True, True, True]
                for move in range(1, 8):
                    # Up
                    if self.player_turn == 'white' and self.board_map[y][x][0:1] == 'w':
                        direction[0] = self.piece_path(direction[0], 'b', 0, -move)
                    elif self.player_turn == 'black' and self.board_map[y][x][0:1] == 'b':
                        direction[0] = self.piece_path(direction[0], 'w', 0, -move)
                    # Right
                    if self.player_turn == 'white' and self.board_map[y][x][0:1] == 'w':
                        direction[1] = self.piece_path(direction[1], 'b', move, 0)
                    elif self.player_turn == 'black' and self.board_map[y][x][0:1] == 'b':
                        direction[1] = self.piece_path(direction[1], 'w', move, 0)
                    # Left
                    if self.player_turn == 'white' and self.board_map[y][x][0:1] == 'w':
                        direction[2] = self.piece_path(direction[2], 'b', 0, move)
                    elif self.player_turn == 'black' and self.board_map[y][x][0:1] == 'b':
                        direction[2] = self.piece_path(direction[2], 'w', 0, move)
                    # Down
                    if self.player_turn == 'white' and self.board_map[y][x][0:1] == 'w':
                        direction[3] = self.piece_path(direction[3], 'b', -move, 0)
                    elif self.player_turn == 'black' and self.board_map[y][x][0:1] == 'b':
                        direction[3] = self.piece_path(direction[3], 'w', -move, 0)

    def queen_move(self):
        # Queen next moves
        if self.selected_piece != None:
            if self.selected_piece[2:5] == 'qn':
                x = self.click_position[0]
                y = self.click_position[1]
                direction = [True, True, True, True, True, True, True, True]
                for move in range(1, 8):
                    # Up
                    if self.player_turn == 'white' and self.board_map[y][x][0:1] == 'w':
                        direction[0] = self.piece_path(direction[0], 'b', 0, -move)
                    elif self.player_turn == 'black' and self.board_map[y][x][0:1] == 'b':
                        direction[0] = self.piece_path(direction[0], 'w', 0, -move)
                    # Up + Right
                    if self.player_turn == 'white' and self.board_map[y][x][0:1] == 'w':
                        direction[1] = self.piece_path(direction[1], 'b', move, -move)
                    elif self.player_turn == 'black' and self.board_map[y][x][0:1] == 'b':
                        direction[1] = self.piece_path(direction[1], 'w', move, -move)
                    # Right
                    if self.player_turn == 'white' and self.board_map[y][x][0:1] == 'w':
                        direction[2] = self.piece_path(direction[2], 'b', move, 0)
                    elif self.player_turn == 'black' and self.board_map[y][x][0:1] == 'b':
                        direction[2] = self.piece_path(direction[2], 'w', move, 0)
                    # Down + Right
                    if self.player_turn == 'white' and self.board_map[y][x][0:1] == 'w':
                        direction[3] = self.piece_path(direction[3], 'b', move, move)
                    elif self.player_turn == 'black' and self.board_map[y][x][0:1] == 'b':
                        direction[3] = self.piece_path(direction[3], 'w', move, move)
                    # Down
                    if self.player_turn == 'white' and self.board_map[y][x][0:1] == 'w':
                        direction[4] = self.piece_path(direction[4], 'b', 0, move)
                    elif self.player_turn == 'black' and self.board_map[y][x][0:1] == 'b':
                        direction[4] = self.piece_path(direction[4], 'w', 0, move)
                    # Down + Left
                    if self.player_turn == 'white' and self.board_map[y][x][0:1] == 'w':
                        direction[5] = self.piece_path(direction[5], 'b', -move, move)
                    elif self.player_turn == 'black' and self.board_map[y][x][0:1] == 'b':
                        direction[5] = self.piece_path(direction[5], 'w', -move, move)
                    # Left
                    if self.player_turn == 'white' and self.board_map[y][x][0:1] == 'w':
                        direction[6] = self.piece_path(direction[6], 'b', -move, 0)
                    elif self.player_turn == 'black' and self.board_map[y][x][0:1] == 'b':
                        direction[6] = self.piece_path(direction[6], 'w', -move, 0)
                    # Up + Left
                    if self.player_turn == 'white' and self.board_map[y][x][0:1] == 'w':
                        direction[7] = self.piece_path(direction[7], 'b', -move, -move)
                    elif self.player_turn == 'black' and self.board_map[y][x][0:1] == 'b':
                        direction[7] = self.piece_path(direction[7], 'w', -move, -move)

    def is_opposing_piece_checking_the_king(self, path, opposing_piece, x, y, step_x, step_y):
        if x + step_x <= -1 or y + step_y <= -1:
            return False, False
        elif x + step_x >= 8 or y + step_y >= 8:
            return False, False

        if  opposing_piece[0:1] == 'w':
            king = 'b_kg'
        else:
            king = 'w_kg'

        if path:
            if self.board_map[y+step_y][x+step_x] == opposing_piece:
                return False, True
            elif self.board_map[y+step_y][x+step_x] == king:
                return True, False
            elif self.board_map[y+step_y][x+step_x] == '':
                return True, False
            elif self.board_map[y+step_y][x+step_x] != '':
                return False, False
        else:
            return False, False

    def is_bishop_checking_the_king(self, opposing_piece, x, y):
        check = [False, False, False, False]
        final_check = False
        direction = [True, True, True, True]
        for move in range(1, 8):
            direction[0], check_pivot = self.is_opposing_piece_checking_the_king(direction[0], opposing_piece+'_bs', x, y, move, -move)
            if direction[0] == False and check_pivot == True:
                check[0] = True
            direction[1], check_pivot = self.is_opposing_piece_checking_the_king(direction[1], opposing_piece+'_bs', x, y, move, move)
            if direction[1] == False and check_pivot == True:
                check[1] = True
            direction[2], check_pivot = self.is_opposing_piece_checking_the_king(direction[2], opposing_piece+'_bs', x, y, -move, move)
            if direction[2] == False and check_pivot == True:
                check[2] = True
            direction[3], check_pivot = self.is_opposing_piece_checking_the_king(direction[3], opposing_piece+'_bs', x, y, -move, -move)
            if direction[3] == False and check_pivot == True:
                check[3] = True
        if check[0] == True or check[2] == True:
            final_check = True
        elif check[1] == True or check[3] == True:
            final_check = True
        return final_check

    def is_rook_checking_the_king(self, opposing_piece, x, y):
        check = [False, False, False, False]
        final_check = False
        direction = [True, True, True, True]
        for move in range(1, 8):
            direction[0], check_pivot = self.is_opposing_piece_checking_the_king(direction[0], opposing_piece+'_rk', x, y, 0, -move)
            if direction[0] == False and check_pivot == True:
                check[0] = True
            direction[1], check_pivot = self.is_opposing_piece_checking_the_king(direction[1], opposing_piece+'_rk', x, y, move, 0)
            if direction[1] == False and check_pivot == True:
                check[1] = True
            direction[2], check_pivot = self.is_opposing_piece_checking_the_king(direction[2], opposing_piece+'_rk', x, y, 0, move)
            if direction[2] == False and check_pivot == True:
                check[2] = True
            direction[3], check_pivot = self.is_opposing_piece_checking_the_king(direction[3], opposing_piece+'_rk', x, y, -move, 0)
            if direction[3] == False and check_pivot == True:
                check[3] = True
        if check[0] == True or check[2] == True:
            final_check = True
        elif check[1] == True or check[3] == True:
            final_check = True
        return final_check

    def is_queen_checking_the_king(self, opposing_piece, x, y):
        check = [False, False, False, False, False, False, False, False]
        final_check = False
        direction = [True, True, True, True, True, True, True, True]
        for move in range(1, 8):
            direction[0], check_pivot = self.is_opposing_piece_checking_the_king(direction[0], opposing_piece+'_qn', x, y, 0, -move)
            if direction[0] == False and check_pivot == True:
                check[0] = True
            direction[1], check_pivot = self.is_opposing_piece_checking_the_king(direction[1], opposing_piece+'_qn', x, y, move, 0)
            if direction[1] == False and check_pivot == True:
                check[1] = True
            direction[2], check_pivot = self.is_opposing_piece_checking_the_king(direction[2], opposing_piece+'_qn', x, y, 0, move)
            if direction[2] == False and check_pivot == True:
                check[2] = True
            direction[3], check_pivot = self.is_opposing_piece_checking_the_king(direction[3], opposing_piece+'_qn', x, y, -move, 0)
            if direction[3] == False and check_pivot == True:
                check[3] = True
            direction[4], check_pivot = self.is_opposing_piece_checking_the_king(direction[4], opposing_piece+'_qn', x, y, move, -move)
            if direction[4] == False and check_pivot == True:
                check[4] = True
            direction[5], check_pivot = self.is_opposing_piece_checking_the_king(direction[5], opposing_piece+'_qn', x, y, move, move)
            if direction[5] == False and check_pivot == True:
                check[5] = True
            direction[6], check_pivot = self.is_opposing_piece_checking_the_king(direction[6], opposing_piece+'_qn', x, y, -move, move)
            if direction[6] == False and check_pivot == True:
                check[6] = True
            direction[7], check_pivot = self.is_opposing_piece_checking_the_king(direction[7], opposing_piece+'_qn', x, y, -move, -move)
            if direction[7] == False and check_pivot == True:
                check[7] = True
        if check[0] == True or check[2] == True:
            final_check = True
        elif check[1] == True or check[3] == True:
            final_check = True
        elif check[4] == True or check[6] == True:
            final_check = True
        elif check[5] == True or check[7] == True:
            final_check = True
        return final_check

    def is_knight_checking_the_king(self, opposing_piece, x, y):
        moves = [[1, 2], [2, 1], [2, -1], [1, -2], [-1, -2], [-2, -1], [-2, 1], [-1 , 2]]
        for move in moves:
            if y+move[0] <= 7 and x+move[1] <= 7 and y+move[0] >= 0 and x+move[1] >= 0:
                if self.board_map[y+move[0]][x+move[1]] == opposing_piece+'_kn':
                    return True
            else:
                continue
        return False

    def is_pawn_checking_the_king(self, opposing_piece, x, y):
        check_left = True
        check_right = True
        check_up = True
        check_down = True
        if x - 1 <= -1:
            check_left = False
        if y - 1 <= -1:
            check_up = False
        if x + 1 >= 8:
            check_right = False
        if y + 1 >= 8:
            check_down = False

        if self.player_view == 'white' and opposing_piece == 'b':
            if check_left and check_up:
                if self.board_map[y-1][x-1] == opposing_piece+'_pw':
                    return True
            if check_up and check_right:
                if self.board_map[y-1][x+1] == opposing_piece+'_pw':
                    return True
        elif self.player_view == 'white' and opposing_piece == 'w':
            if check_left and check_down:
                if self.board_map[y+1][x-1] == opposing_piece+'_pw':
                    return True
            if check_down and check_right:
                if self.board_map[y+1][x+1] == opposing_piece+'_pw':
                    return True
        elif self.player_view == 'black' and opposing_piece == 'b':
            if check_left and check_down:
                if self.board_map[y+1][x-1] == opposing_piece+'_pw':
                    return True
            if check_down and check_right:
                if self.board_map[y+1][x+1] == opposing_piece+'_pw':
                    return True
        elif self.player_view == 'black' and opposing_piece == 'w':
            if check_left and check_up:
                if self.board_map[y-1][x-1] == opposing_piece+'_pw':
                    return True
            if check_up and check_right:
                if self.board_map[y-1][x+1] == opposing_piece+'_pw':
                    return True

    def is_other_king_checking_the_king(self, opposing_piece, x, y):
        check = False
        for yy in range(-1, 2):
            for xx in range(-1, 2):
                try:
                    if self.board_map[y+yy][x+xx] == opposing_piece+'_kg':
                        check = True
                except:
                    continue
        return check

    def is_king_in_check(self, opposing_piece, x, y):
        check = False

        if self.is_bishop_checking_the_king(opposing_piece, x, y):
            check = True
        elif self.is_rook_checking_the_king(opposing_piece, x, y):
            check = True
        elif self.is_queen_checking_the_king(opposing_piece, x, y):
            check = True
        elif self.is_knight_checking_the_king(opposing_piece, x, y):
            check = True
        elif self.is_pawn_checking_the_king(opposing_piece, x, y):
            check = True
        elif self.is_other_king_checking_the_king(opposing_piece, x, y):
            check = True

        return check

    def king_move(self):
        # King next moves
        if self.selected_piece != None:
            if self.selected_piece[2:5] == 'kg':
                x = self.click_position[0]
                y = self.click_position[1]
                if self.player_turn == 'white' and self.board_map[y][x][0:1] == 'w':
                    # Up
                    if self.is_king_in_check('b', x, y-1) == False:
                        _ = self.piece_path(True, 'b', 0, -1)
                    # Up + Right
                    if self.is_king_in_check('b', x+1, y-1) == False:
                        _ = self.piece_path(True, 'b', 1, -1)
                    # Right
                    if self.is_king_in_check('b', x+1, y) == False:
                        _ = self.piece_path(True, 'b', 1, 0)
                    # Down + Right
                    if self.is_king_in_check('b', x+1, y+1) == False:
                        _ = self.piece_path(True, 'b', 1, 1)
                    # Down
                    if self.is_king_in_check('b', x, y+1) == False:
                        _ = self.piece_path(True, 'b', 0, 1)
                    # Down Left
                    if self.is_king_in_check('b', x-1, y+1) == False:
                        _ = self.piece_path(True, 'b', -1, 1)
                    # Left
                    if self.is_king_in_check('b', x-1, y) == False:
                        _ = self.piece_path(True, 'b', -1, 0)
                    # Up + Left
                    if self.is_king_in_check('b', x-1, y-1) == False:
                        _ = self.piece_path(True, 'b', -1, -1)
                elif self.player_turn == 'black' and self.board_map[y][x][0:1] == 'b':
                    # Up
                    if self.is_king_in_check('w', x, y-1) == False:
                        _ = self.piece_path(True, 'w', 0, -1)
                    # Up + Right
                    if self.is_king_in_check('w', x+1, y-1) == False:
                        _ = self.piece_path(True, 'w', 1, -1)
                    # Right
                    if self.is_king_in_check('w', x+1, y) == False:
                        _ = self.piece_path(True, 'w', 1, 0)
                    # Down + Right
                    if self.is_king_in_check('w', x+1, y+1) == False:
                        _ = self.piece_path(True, 'w', 1, 1)
                    # Down
                    if self.is_king_in_check('w', x, y+1) == False:
                        _ = self.piece_path(True, 'w', 0, 1)
                    # Down + Left
                    if self.is_king_in_check('w', x-1, y+1) == False:
                        _ = self.piece_path(True, 'w', -1, 1)
                    # Left
                    if self.is_king_in_check('w', x-1, y) == False:
                        _ = self.piece_path(True, 'w', -1, 0)
                    # Up + Left
                    if self.is_king_in_check('w', x-1, y-1) == False:
                        _ = self.piece_path(True, 'w', -1, -1)
                self.castling_path()

    def mouse_actions(self, mouse):
        # Board clicks
        mx, my = mouse[0]
        if getattr(self, 'game_over', False):
            return
        if mouse[2][0] == True:
            for y in range(8):
                for x in range(8):
                    if mx >= (x * 100) and mx <= (x * 100) + 100 and my >= (y * 100) and my <= (y * 100) + 100:
                        if self.click_position != None:
                            last_x = self.click_position[0]
                            last_y = self.click_position[1]
                            self.last_click_position = [last_x, last_y]
                            self.last_selected_piece = self.board_map[last_y][last_x]
                        self.selected_piece = self.board_map[y][x]
                        self.click_position = [x, y]

    def new_game(self):
        self.player_view = 'white'
        self.player_turn = 'white'
        self.selected_piece = None
        self.last_selected_piece = None
        self.click_position = None
        self.last_click_position = None
        self.en_passant = None
        self.white_castling_movement_condition = [True, True, True]
        self.black_castling_movement_condition = [True, True, True]
        # Reset game state
        self.game_over = False
        self.in_check = False
        self.winner = None
        self.game_result = ''
        # Reset history
        self.move_history = []
        self.state_history = []
        self.prev_in_check = False

        self.board_map = [['b_rk','b_kn','b_bs','b_qn','b_kg','b_bs','b_kn','b_rk'],
                          ['b_pw','b_pw','b_pw','b_pw','b_pw','b_pw','b_pw','b_pw'],
                          [    '',    '',    '',    '',    '',    '',    '',    ''],
                          [    '',    '',    '',    '',    '',    '',    '',    ''],
                          [    '',    '',    '',    '',    '',    '',    '',    ''],
                          [    '',    '',    '',    '',    '',    '',    '',    ''],
                          ['w_pw','w_pw','w_pw','w_pw','w_pw','w_pw','w_pw','w_pw'],
                          ['w_rk','w_kn','w_bs','w_qn','w_kg','w_bs','w_kn','w_rk']]

        self.actions_board_map = [['','','','','','','',''],
                                  ['','','','','','','',''],
                                  ['','','','','','','',''],
                                  ['','','','','','','',''],
                                  ['','','','','','','',''],
                                  ['','','','','','','',''],
                                  ['','','','','','','',''],
                                  ['','','','','','','','']]

    def rotate_board(self):
        # Flip board view
        self.board_map = [row[::-1] for row in self.board_map[::-1]]
        # Flip variable click_position
        if self.click_position != None:
            self.click_position = [7 - self.click_position[0], 7 - self.click_position[1]]
        # Flip variable last_click_position
        if self.last_click_position != None:
            self.last_click_position = [7 - self.last_click_position[0], 7 - self.last_click_position[1]]
        # Flip en_passant variable position
        if self.en_passant != None:
            self.en_passant = [7 - self.en_passant[0], 7 - self.en_passant[1]]
        # Flip castling variable position
        pivot = self.white_castling_movement_condition[0]
        self.white_castling_movement_condition[0] = self.white_castling_movement_condition[2]
        self.white_castling_movement_condition[2] = pivot
        pivot = self.black_castling_movement_condition[0]
        self.black_castling_movement_condition[0] = self.black_castling_movement_condition[2]
        self.black_castling_movement_condition[2] = pivot
        # Change board view variable
        if self.player_view == 'white':
            self.player_view = 'black'
        elif self.player_view == 'black':
            self.player_view = 'white'
        # On rotate, update status messages
        self.update_check_and_game_state()

    def actions(self, key):
        if key == 'r':
            self.rotate_board()
        if key == 'n':
            self.new_game()
        if key == 'u':
            self.undo_move()


def main():
    jogo = Chess()

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                quit()
            if event.type == pg.KEYDOWN:
                jogo.actions(pg.key.name(event.key))
                if pg.key.name(event.key) == 'escape':
                    pg.quit()
                    quit()

        # Mouse info
        mouse_position  = pg.mouse.get_pos()
        mouse_input = pg.mouse.get_pressed()
        mouse_click = jogo.mouse_has_clicked(mouse_input)
        mouse = (mouse_position, mouse_input, mouse_click)

        # Game
        jogo.clock.tick(60)
        jogo.board()
        jogo.mouse_actions(mouse)
        jogo.piece_move_or_capture()
        jogo.clear_map_actions()
        jogo.pawn_move()
        jogo.knight_move()
        jogo.bishop_move()
        jogo.rook_move()
        jogo.queen_move()
        jogo.king_move()

        # Filter out illegal moves (those leaving the king in check) for the selected piece
        jogo.filter_moves_for_selected()

        # Update check / checkmate / stalemate state
        jogo.update_check_and_game_state()

        # Update display
        pg.display.flip()


if __name__ == '__main__':
    main()