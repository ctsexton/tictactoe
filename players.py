from copy import deepcopy
from helpers import check_set
from operator import itemgetter

class Human:
    def choose_square(self, board):
        return input('\nPlace mark in box: ')

class Computer:
    def choose_square(self, board):
        empty_squares = board.get_empty()
        moves = list(map(lambda square: {'square': square, 'score': self.score(x, board)}, empty_squares))
        bestMove = sorted(moves, key=itemgetter('score'), reverse=True)
        if bestMove[0].score == 2:
            self.score(bestMove[0].square)

    def score(self, index, board):
        new_board = deepcopy(board)
        position = Point(index, new_board.nrows, new_board.ncolumns)
        new_board.mark(position.x, position.y, 2)
        score = self.terminal_state(new_board)
        return score

    def evaluate_board(self, board):
        if check_set(board.columns()):
            return True
        if check_set(board.rows()):
            return True
        if check_set(board.diagonals()):
            return True
        return False

    def terminal_state(self, board, player):
        if self.evaluate_board(board) == True and player == 1:
            return 1 # Win
        if self.evaluate_board(board) == True and player == 2:
            return -1 # Win
        if board.get_empty() == []:
            return 0 # Tie
        return 2 # Incomplete

class Point:
    def __init__(self, index, rows, columns):
        self.x = index % columns
        self.y = index // columns
        self.number = index

    def coordinates(self):
        return [self.x, self.y]



