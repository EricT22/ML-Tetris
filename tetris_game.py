import cfg
from bag import Bag
from pieces import Piece
from board import Board_Panel
from IllegalMoveError import IllegalMoveError

class Tetris_Game:
    def __init__(self) -> None:
        self.board = Board_Panel(cfg.TETRIS_TILE_SIZE, cfg.TETRIS_ROWS, cfg.TETRIS_COLS, cfg.MAIN_BOARD_X_OFFSET, cfg.MAIN_BOARD_Y_OFFSET)
        self.next_board = Board_Panel(cfg.TETRIS_TILE_SIZE, cfg.SQUARE_PANEL_SIZE, cfg.SQUARE_PANEL_SIZE, cfg.NEXT_PANEL_X_OFFSET, cfg.NEXT_PANEL_Y_OFFSET)
        self.hold_board = Board_Panel(cfg.TETRIS_TILE_SIZE, cfg.SQUARE_PANEL_SIZE, cfg.SQUARE_PANEL_SIZE, cfg.HOLD_PANEL_X_OFFSET, cfg.HOLD_PANEL_Y_OFFSET)
        self.bag = Bag()
        self.cur_piece: Piece = self.bag.get_next_piece()
        self.next_piece: Piece = self.bag.get_next_piece()
        self.next_piece.set_center(cfg.PIECE_SIDE_PANEL_X, cfg. PIECE_SIDE_PANEL_Y)
        self.held_piece: Piece = None
        self.hold_lock_out = False
        self.piece_in_play = True
        self.game_over = False
        self.level_up_triggered = False
        self.level = 1
        self.score = 0
        self.lines = 0


        self.actions = {
            0 : (self.move_piece_down, cfg.SCORE_PER_MOVE_DOWN),
            1 : (self.auto_down, cfg.SCORE_PER_AUTO_DOWN),
            2 : (self.move_piece_sideways, True),
            3 : (self.move_piece_sideways, False),
            4 : (self.rotate_piece, True),
            5 : (self.rotate_piece, False),
            6 : self.hold
        }

        self.board_for_calc = list(self.board.game_board)

    
    # Machine Learning methods
    def reset(self):
        # restart game, return state
        pass


    def step(self, action):
        # take action, returns (next_state, reward, done) where done is a flag that is set if the game is over
        pass


    def get_state(self):
        # state is a combination of number of holes, bumpiness, max height, min height, and lines cleared
        pass


    def state_properties(self, board) -> tuple[int, int, int, int]:
        heights = []
        num_holes = 0
        
        for col in zip(*board):
            row = 0
            
            while row < cfg.TETRIS_ROWS and col[row] == 0:
                row += 1
            
            heights.append(cfg.TETRIS_ROWS - row)

            while row < cfg.TETRIS_ROWS:
                if col[row] == 0:
                    num_holes += 1
                row += 1

        # bumpiness is difference in adjacent heights
        bumpiness = 0
        for i in range(1, cfg.TETRIS_COLS, 1):
            bumpiness += abs(heights[i] - heights[i - 1])

        return (num_holes, bumpiness, max(heights), min(heights))




    # Game methods
    def draw(self, screen) -> None:
        if self.piece_in_play and not self.game_over:
            self.cur_piece.draw_on_board(self.board)
            self.next_piece.draw_on_board(self.next_board)
        self.board.draw(screen)
        self.next_board.draw(screen)
        self.hold_board.draw(screen)


    def hold(self):
        if not self.hold_lock_out:
            self.cur_piece.remove_piece_from_board(self.board)

            if self.held_piece is None:
                self.held_piece = self.cur_piece
                
                if not self._spawn_new_piece(hold_flag_set=True):
                    self.held_piece = None
                    self.cur_piece.draw_on_board(self.board)
                    return
            else:
                temp = self.cur_piece
                self.cur_piece = self.held_piece
                self.cur_piece.set_center(cfg.PIECE_STARTING_X, cfg.PIECE_STARTING_Y)

                try:
                    self.cur_piece.is_action_possible(self.board)
                    self.cur_piece.draw_on_board(self.board)
                except IllegalMoveError:
                    self.cur_piece = temp
                    self.cur_piece.draw_on_board(self.board)
                    return
                
                self.held_piece = temp
            
            self.held_piece.set_center(cfg.PIECE_SIDE_PANEL_X, cfg.PIECE_SIDE_PANEL_Y)
            self.held_piece.set_orientation(cfg.DEFAULT_ORIENTATION)

            self.hold_board.clear()
            self.held_piece.draw_on_board(self.hold_board)
            
            self.hold_lock_out = True


    def move_piece_down(self, score_per_move: int):
        if not self.game_over:    
            if self.piece_in_play:
                try:
                    self.cur_piece.move_down(self.board)
                    self.score += score_per_move
                except IllegalMoveError:
                    self.piece_in_play = False
            else:
                lines_cleared = self._check_line_clear()
                self.update_counters(lines_cleared)
                self._spawn_new_piece()


    def auto_down(self, score_per_move: int):
        while self.piece_in_play and not self.game_over:
            self.move_piece_down(score_per_move)


    def move_piece_sideways(self, move_right: bool):
        if self.piece_in_play and not self.game_over:
            self.cur_piece.move_sideways(self.board, move_right)


    def rotate_piece(self, rotate_right: bool):
        if self.piece_in_play and not self.game_over and self.cur_piece.name != 5: # 5 == O piece
            self.cur_piece.rotate(self.board, rotate_right)


    def update_counters(self, lines_cleared: int):

        match lines_cleared:
            case 0: line_score = 0
            case 1: line_score = 100 * self.level
            case 2: line_score = 300 * self.level
            case 3: line_score = 500 * self.level
            case 4: line_score = 800 * self.level
        
        self.score += line_score

        for i in range(lines_cleared):
            self.lines += 1
            if self.lines != 0 and self.lines % cfg.LINES_PER_LEVEL_UP == 0:
                self.level += 1
                self.level_up_triggered = True


    def restart_game(self):
        self.board.clear()
        self.bag.refill()
        self.next_piece = self.bag.get_next_piece()
        self._spawn_new_piece()

        self.level = 1
        self.score = 0
        self.lines = 0

        self.hold_lock_out = False

        self.game_over = False



    # helper functions
    def _spawn_new_piece(self, hold_flag_set=False) -> bool:
        if not hold_flag_set and self.hold_lock_out:
            self.hold_lock_out = False

        self.cur_piece = self.next_piece
        self.cur_piece.set_center(cfg.PIECE_STARTING_X, cfg. PIECE_STARTING_Y)

        self.next_piece = self.bag.get_next_piece()
        self.next_piece.set_center(cfg.PIECE_SIDE_PANEL_X, cfg.PIECE_SIDE_PANEL_Y)

        try:
            self.cur_piece.is_action_possible(self.board)
            self.cur_piece.draw_on_board(self.board)
            
            
            self.next_board.clear()
            self.next_piece.draw_on_board(self.next_board)
            
            self.piece_in_play = True

            return True
        except IllegalMoveError:
            if not hold_flag_set:
                self.game_over = True

            return False


    def _check_line_clear(self) -> int:
        lines_cleared = 0
        row = len(self.board.game_board) - 1

        while row >= 0:
            if self._row_filled(row):
                self._remove_row(row)
                lines_cleared += 1
                row += 1
            
            row -= 1
        
        return lines_cleared
    
    def _row_filled(self, row):
        for c in self.board.game_board[row]:
            if c == 0:
                return False
            
        return True
    
    def _remove_row(self, row):
        for i in range(row, 0, -1):
            for j in range(self.board.cols):
                self.board.game_board[i][j] = self.board.game_board[i - 1][j]
        