from copy import deepcopy
from helpers import check_set

class Human:
    def choose_square(self, board):
        return input('\nPlace mark in box: ')

class Computer:
    def choose_square(self, board):
        empty_squares = board.get_empty()
        moves = list(map(lambda x: {'square': x, 'score': self.score(x, board)}, empty_squares))
        print(moves)

    def score(self, index, board):
        new_board = deepcopy(board)
        position = Point(index, new_board.nrows, new_board.ncolumns)
        new_board.mark(position.x, position.y, 2)
        result = self.evaluate_board(new_board)
        if result == True:
            return 'WIN'
        else:
            return 'LOSE'

    def evaluate_board(self, board):
        if check_set(board.columns()):
            return True
        if check_set(board.rows()):
            return True
        if check_set(board.diagonals()):
            return True
        return False
class Point:
    def __init__(self, index, rows, columns):
        self.x = index % columns
        self.y = index // columns
        self.number = index

    def coordinates(self):
        return [self.x, self.y]



