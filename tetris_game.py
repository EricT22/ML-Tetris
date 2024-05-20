from bag import Bag
from board import Board

class Tetris_Game:
    def __init__(self) -> None:
        self.board = Board()
        # self.bag = Bag()
        # self.cur_piece = self.bag.get_next_piece()
    
    def draw(self, screen) -> None:
        self.board.draw(screen)
        # self.cur_piece.draw(screen)