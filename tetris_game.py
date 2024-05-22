from bag import Bag
from pieces import Piece
# from pieces import *
from board import Board
from IllegalMoveError import IllegalMoveError

class Tetris_Game:
    def __init__(self) -> None:
        self.board = Board()
        self.bag = Bag()
        self.cur_piece: Piece = self.bag.get_next_piece()
        # self.cur_piece = O()
        self.piece_in_play = True
    
    def draw(self, screen) -> None:
        self.cur_piece.draw_on_board(self.board)
        self.board.draw(screen)

    def move_piece_down(self):
        if self.piece_in_play:
            try:
                self.cur_piece.move_down(self.board)
            except IllegalMoveError:
                self.piece_in_play = not self.piece_in_play
    
    def auto_down(self):
        while self.piece_in_play:
            self.move_piece_down()

    def move_piece_sideways(self, move_right: bool):
        if self.piece_in_play:
            self.cur_piece.move_sideways(self.board, move_right)