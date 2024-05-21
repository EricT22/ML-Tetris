from board import Board
from point import Point

class Piece:
    def __init__(self) -> None:
        self.name = ""
        self.center = Point(4, 1)
        self.orientation = 0
        self.piece_constants: list[list[Point]] = []
    
    def draw_on_board(self, board: Board):
        for i in range(len(self.piece_constants[self.orientation])):
                board.update_board(self.center.getY() + self.piece_constants[self.orientation][i].getY(), 
                                   self.center.getX() + self.piece_constants[self.orientation][i].getX(),
                                   self.name)

class T(Piece):
    def __init__(self) -> None:
        super().__init__()

        self.name = "T"

        self.piece_constants = [
            [Point(0, 0), Point(1, 0), Point(-1, 0), Point(0, -1)],
            [Point(0, 0), Point(0, 1), Point(0, -1), Point(1, 0)],
            [Point(0, 0), Point(-1, 0), Point(1, 0), Point(0, 1)],
            [Point(0, 0), Point(0, -1), Point(0, 1), Point(-1, 0)]
        ]

class L(Piece):
    def __init__(self) -> None:
        super().__init__()

        self.name = "L"

        self.piece_constants = [
            [Point(0, 0), Point(1, 0), Point(-1, 0), Point(1, -1)],
            [Point(0, 0), Point(0, 1), Point(0, -1), Point(1, 1)],
            [Point(0, 0), Point(-1, 0), Point(1, 0), Point(-1, 1)],
            [Point(0, 0), Point(0, -1), Point(0, 1), Point(-1, -1)]
        ]

class J(Piece):
    def __init__(self) -> None:
        super().__init__()

        self.name = "J"

        self.piece_constants = [
            [Point(0, 0), Point(1, 0), Point(-1, 0), Point(-1, -1)],
            [Point(0, 0), Point(0, 1), Point(0, -1), Point(1, -1)],
            [Point(0, 0), Point(-1, 0), Point(1, 0), Point(1, 1)],
            [Point(0, 0), Point(0, -1), Point(0, 1), Point(-1, 1)]
        ]


class O(Piece):
    def __init__(self) -> None:
        super().__init__()

        self.name = "O"

        self.piece_constants = [
            [Point(0, 0), Point(1, 0), Point(0, -1), Point(1, -1)],
        ]

class S(Piece):
    def __init__(self) -> None:
        super().__init__()

        self.name = "S"

        self.piece_constants = [
            [Point(0, 0), Point(1, -1), Point(-1, 0), Point(0, -1)],
            [Point(0, 0), Point(1, 1), Point(0, -1), Point(1, 0)],
            [Point(0, 0), Point(-1, 1), Point(1, 0), Point(0, 1)],
            [Point(0, 0), Point(-1, -1), Point(0, 1), Point(-1, 0)]
        ]

class Z(Piece):
    def __init__(self) -> None:
        super().__init__()

        self.name = "Z"

        self.piece_constants = [
            [Point(0, 0), Point(-1, -1), Point(1, 0), Point(0, -1)],
            [Point(0, 0), Point(1, -1), Point(0, 1), Point(1, 0)],
            [Point(0, 0), Point(1, 1), Point(-1, 0), Point(0, 1)],
            [Point(0, 0), Point(-1, 1), Point(0, -1), Point(-1, 0)]
        ]

class I(Piece):
    def __init__(self) -> None:
        super().__init__()

        self.name = "I"

        self.piece_constants = [
            [Point(0, 0), Point(1, 0), Point(2, 0), Point(-1, 0)],
            [Point(1, 0), Point(1, 1), Point(1, 2), Point(1, -1)],
            [Point(1, 1), Point(0, 1), Point(-1, 1), Point(2, 1)],
            [Point(0, 1), Point(0, 0), Point(0, -1), Point(0, 2)]
        ]