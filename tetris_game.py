import cfg
from bag import Bag
from pieces import Piece
from board import Board_Panel
from point import Point
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

        self.state_size = 5
        self.board_for_calc = Board_Panel(0, cfg.TETRIS_ROWS, cfg.TETRIS_COLS, 0, 0)
        self.actions = {
            0 : (self.move_piece_down, cfg.SCORE_PER_MOVE_DOWN),
            1 : (self.auto_down, cfg.SCORE_PER_AUTO_DOWN),
            2 : (self.move_piece_sideways, True),
            3 : (self.move_piece_sideways, False),
            4 : (self.rotate_piece, True),
            5 : (self.rotate_piece, False),
            6 : self.hold
        }

    
    # Machine Learning methods
    def reset(self):
        # restart game, returns state 
        # (no need to calculate the state because the board is empty so all properties have to be 0)
        
        self.restart_game()
        
        return [0, 0, 0, 0, 0]




    def step(self, actions: list):
        # takes actions to get to the best next state, 
        # returns (reward, done) 
        # where reward is the total score of the combined moves
        # and done is a flag that is set if the game is over
        initial_score = self.score

        for i in range(actions[0]):
            action, param = self.actions[4]
            action(param)
        
        x_offset = actions[1]

        if x_offset > 0:
            # move right
            while x_offset > 0:
                action, param = self.actions[2]
                action(param)

                x_offset -= 1
        elif x_offset < 0:
            # move left
            while x_offset < 0:
                action, param = self.actions[3]
                action(param)

                x_offset += 1
        
        # move all the way down
        action, param = self.actions[1]
        action(param)

        # if program is too slow to run at live speed, these lines spawn the new piece in
        # funct, param = self.actions[0]
        # funct(param)
        
        return (self.score - initial_score, self.game_over)




    # returns states dictionary with key value pair:
    # (num rotations, x-offset) : tuple of state properties
    # in other words, 
    # actions to get to state : state itself
    def get_next_states(self):
        # state is a combination of number of holes, bumpiness, max height, min height, and lines cleared
        beginning_center = Point(self.cur_piece.center.getX(), self.cur_piece.center.getY())

        self.board_for_calc.game_board = self.board.copy_of_board()

        states = {}

        num_rotations = 4 if self.cur_piece.name != 5 else 1

        for i in range(num_rotations):
            # move all the way to the left
            while self.cur_piece.move_sideways(self.board_for_calc, False):
                pass
            
            while True:
                try:
                    while self.cur_piece.move_down(self.board_for_calc):
                        pass
                except IllegalMoveError:
                    # here, the piece will be as far down as it can go and we can evaluate the state
                    
                    states[(i, self.cur_piece.center.getX() - beginning_center.getX())] = self.state_properties(self.board_for_calc.game_board)

                # move piece back up
                self.cur_piece.remove_piece_from_board(self.board_for_calc)
                self.cur_piece.set_center(self.cur_piece.center.getX(), beginning_center.getY())
                self.cur_piece.draw_on_board(self.board_for_calc)

                # move piece to the right
                if not self.cur_piece.move_sideways(self.board_for_calc, True):
                    break
            
            # move back to starting pos and rotate
            self.cur_piece.remove_piece_from_board(self.board_for_calc)
            self.cur_piece.set_center(beginning_center.getX(), beginning_center.getY())
            self.cur_piece.draw_on_board(self.board_for_calc)

            if self.cur_piece.name != 5:
                # try to rotate to the right if possible if not, 
                # piece is reset to beginning orientation and calculations are complete
                if not self.cur_piece.rotate(self.board_for_calc, True):
                    for j in range(i):
                        self.cur_piece.rotate(self.board_for_calc, False)
                    
                    break


        return states



    
    def state_properties(self, game_board) -> list[int, int, int, int, int]:
        heights = []
        num_holes = 0
        
        for col in zip(*game_board):
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

        return [num_holes, bumpiness, max(heights), min(heights), self.num_rows_filled(game_board)]


    def num_rows_filled(self, board):
        def line_filled(row):
            for cell in row:
                if cell == 0:
                    return False
                
            return True
        

        num_lines_to_be_cleared = 0

        for i in range(cfg.TETRIS_ROWS):
            if line_filled(board[i]):
                num_lines_to_be_cleared += 1
        
        return num_lines_to_be_cleared




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
        