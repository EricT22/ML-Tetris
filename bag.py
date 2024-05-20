from pieces import *
import random

class Bag:
    def __init__(self) -> None:
        self.pieces = [T(), Z(), S(), L(), J(), I(), O()]
    
    def get_next_piece(self):
        if len(self.pieces) == 0:
            self.refill()

        piece = random.choice(self.pieces)
        self.pieces.remove(piece)
        return piece
    
    def refill(self) -> None:
        self.pieces = [T(), Z(), S(), L(), J(), I(), O()]