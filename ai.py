from copy import deepcopy
from helpers import check_set
from operator import itemgetter
from game import Board, Player
from players import Point
from random import shuffle

def main():
    board = Board(3, 3)

    x = choose_square(board, 1)
    print(x)

def choose_square(board, player):
    empty = board.get_empty()
    moves = list(map(lambda square: get_score(square, board, player), empty))
    shuffle(moves)
    if player == 1:
        bestMove = sorted(moves, key=itemgetter('score'), reverse=True)
    else:
        bestMove = sorted(moves, key=itemgetter('score'))
    return bestMove[0]

def get_score(square, board, player):
    new_board = deepcopy(board)
    position = Point(square, new_board.nrows, new_board.ncolumns)
    new_board.mark(position.x, position.y, player)
    score = state(new_board, player)
    if score == 2:
        new_player = switch_player(player)
        outcome = choose_square(new_board, new_player)
        return {'square': square, 'score': outcome['score']}
    else:
        return {'square': square, 'score': score}
            

def switch_player(player):
    if player == 1:
        return 2
    return 1

def state(board, player):
    if evaluate_board(board) == True and player == 1:
        return 1 # Win
    if evaluate_board(board) == True and player == 2:
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

def evaluate_board(board):
    if check_set(board.columns()):
        return True
    if check_set(board.rows()):
        return True
    if check_set(board.diagonals()):
        return True
    return False

main()
