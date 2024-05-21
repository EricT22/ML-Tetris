from bag import Bag
from pieces import Piece
# from pieces import *
from board import Board

class Tetris_Game:
    def __init__(self) -> None:
        self.board = Board()
        self.bag = Bag()
        self.cur_piece: Piece = self.bag.get_next_piece()
        # self.cur_piece = O()
    
    def draw(self, screen) -> None:
        self.cur_piece.draw_on_board(self.board)
        self.board.draw(screen)