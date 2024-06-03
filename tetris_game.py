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
        self.next_piece.set_center(cfg.PIECE_SIDE_PANEL_X, cfg.PIECE_SIDE_PANEL_Y)
        self.piece_in_play = True
        self.game_over = False
        self.level_up_constant = 10
        self.level = 1
        self.score = 0
        self.lines = 0

    

    def draw(self, screen) -> None:
        if self.piece_in_play and not self.game_over:
            self.cur_piece.draw_on_board(self.board)
            self.next_piece.draw_on_board(self.next_board)
        self.board.draw(screen)
        self.next_board.draw(screen)
        self.hold_board.draw(screen)


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
        if self.piece_in_play and not self.game_over and self.cur_piece.name != 'O':
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
            if self.lines != 0 and self.lines % self.level_up_constant == 0:
                self.level += 1


    def restart_game(self):
        self.board.clear()
        self.bag.refill()
        self.next_piece = self.bag.get_next_piece()
        self._spawn_new_piece()

        self.level = 1
        self.score = 0
        self.lines = 0

        self.game_over = False



    # helper functions
    def _spawn_new_piece(self):
        self.cur_piece = self.next_piece
        self.cur_piece.set_center(cfg.PIECE_STARTING_X, cfg.PIECE_STARTING_Y)

        self.next_piece = self.bag.get_next_piece()
        self.next_piece.set_center(cfg.PIECE_SIDE_PANEL_X, cfg.PIECE_SIDE_PANEL_Y)

        try:
            self.cur_piece.is_action_possible(self.board)
            self.cur_piece.draw_on_board(self.board)

            
            self.next_board.clear()
            self.next_piece.draw_on_board(self.next_board)
            
            self.piece_in_play = True
        except IllegalMoveError:
            self.game_over = True


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
            if c == 'U':
                return False
            
        return True
    
    def _remove_row(self, row):
        for i in range(row, 0, -1):
            for j in range(self.board.cols):
                self.board.game_board[i][j] = self.board.game_board[i - 1][j]
        