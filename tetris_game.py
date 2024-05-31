from bag import Bag
from pieces import Piece
from board import Board
from IllegalMoveError import IllegalMoveError

class Tetris_Game:
    def __init__(self) -> None:
        self.board = Board()
        self.bag = Bag()
        self.cur_piece: Piece = self.bag.get_next_piece()
        self.piece_in_play = True
        self.game_over = False
    

    def draw(self, screen) -> None:
        if self.piece_in_play and not self.game_over:
            self.cur_piece.draw_on_board(self.board)
        self.board.draw(screen)


    def move_piece_down(self):
        if not self.game_over:    
            if self.piece_in_play:
                try:
                    self.cur_piece.move_down(self.board)
                except IllegalMoveError:
                    self.piece_in_play = False
            else:
                self._check_line_clear()
                self._spawn_new_piece()


    def auto_down(self):
        while self.piece_in_play and not self.game_over:
            self.move_piece_down()


    def move_piece_sideways(self, move_right: bool):
        if self.piece_in_play and not self.game_over:
            self.cur_piece.move_sideways(self.board, move_right)


    def rotate_piece(self, rotate_right: bool):
        if self.piece_in_play and not self.game_over and self.cur_piece.name != 'O':
            self.cur_piece.rotate(self.board, rotate_right)
        

    def restart_game(self):
        self.board.clear()
        self.bag.refill()
        self._spawn_new_piece()

        self.game_over = False



    # helper functions
    def _spawn_new_piece(self):
        self.cur_piece = self.bag.get_next_piece()

        try:
            self.cur_piece.is_action_possible(self.board)
            self.cur_piece.draw_on_board(self.board)
            self.piece_in_play = True
        except IllegalMoveError:
            self.game_over = True


    def _check_line_clear(self):
        row = len(self.board.game_board) - 1

        while row >= 0:
            if self._row_filled(row):
                self._remove_row(row)
                row += 1
            
            row -= 1
    
    def _row_filled(self, row):
        for c in self.board.game_board[row]:
            if c == 'U':
                return False
            
        return True
    
    def _remove_row(self, row):
        for i in range(row, 0, -1):
            for j in range(self.board.cols):
                self.board.game_board[i][j] = self.board.game_board[i - 1][j]
        