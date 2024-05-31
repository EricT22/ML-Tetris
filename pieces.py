from board import Board_Panel
from point import Point
from IllegalMoveError import IllegalMoveError

class Piece:
    def __init__(self) -> None:
        self.name = ""
        self.center = Point(4, 1)
        self.orientation = 0
        self.piece_constants: list[list[Point]] = []


    def is_action_possible(self, board: Board_Panel):
        for i in range(len(self.piece_constants[self.orientation])):
            try:
                if board.get_value(self.center.getY() + self.piece_constants[self.orientation][i].getY(), 
                                    self.center.getX() + self.piece_constants[self.orientation][i].getX(),) != 'U':
                    raise IllegalMoveError
            except IndexError:
                raise IllegalMoveError
    

    def draw_on_board(self, board: Board_Panel):
        for i in range(len(self.piece_constants[self.orientation])):
            board.update_board(self.center.getY() + self.piece_constants[self.orientation][i].getY(), 
                                self.center.getX() + self.piece_constants[self.orientation][i].getX(),
                                self.name)
    

    def move_down(self, board: Board_Panel):
        try:
            self._remove_piece_from_board(board)

            self.center.setY(self.center.getY() + 1)

            self.is_action_possible(board)
                
            self.draw_on_board(board)

        except IllegalMoveError:
            self.center.setY(self.center.getY() - 1)
            self.draw_on_board(board)
            raise IllegalMoveError
        

    def move_sideways(self, board: Board_Panel, move_right):
        try:
            self._remove_piece_from_board(board)

            if move_right:
                self.center.setX(self.center.getX() + 1)
            else:
                self.center.setX(self.center.getX() - 1)


            self.is_action_possible(board)

            self.draw_on_board(board)

        except IllegalMoveError:
            if move_right:
                self.center.setX(self.center.getX() - 1)
            else:
                self.center.setX(self.center.getX() + 1)

            self.draw_on_board(board)


    def rotate(self, board: Board_Panel, rotate_right):
        try:
            cur_orientation = self.orientation

            self._remove_piece_from_board(board)

            if rotate_right:
                self.orientation = (self.orientation + 1) % 4
            else:
                self.orientation = (self.orientation - 1 + 4) % 4

            self.is_action_possible(board)
            
            self.draw_on_board(board)
        
        except IllegalMoveError:
            self.orientation = cur_orientation
            self.draw_on_board(board)

    
    def _remove_piece_from_board(self, board: Board_Panel):
        for i in range(len(self.piece_constants[self.orientation])):
            board.update_board(self.center.getY() + self.piece_constants[self.orientation][i].getY(), 
                                self.center.getX() + self.piece_constants[self.orientation][i].getX(),
                                'U')


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