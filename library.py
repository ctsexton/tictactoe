from helpers import clear_console, check_set, nested_groups, check_equal, coord_to_index
from itertools import cycle
from copy import deepcopy
from operator import itemgetter
from random import shuffle

class Game:
    def __init__(self, board, players):
        self.board = board
        symbols = [' ']
        for player in players:
            symbols.append(player.symbol)
        self.ui = UI(symbols)
        self.board = board
        self.players = cycle(players)

    def start(self):
        clear_console()
        self.ui.draw(self.board)
        self.loop(self.board)

    def turn(self):
        next_player = next(self.players)
        print(next_player.name + ': ')
        return next_player

    def loop(self, board):
        move = Move(board)
        player = self.turn()
        result = move.play(player)
        clear_console()
        self.ui.draw(move.board)
        if result is None:
            self.loop(move.board)
        elif result == 'tie':
            self.tie()
        else:
            self.win(player)

    def win(self, player):
        print("\n" + player.name + " WON!!!\n")

    def tie(self):
        print("\nIt was a tie!\n")

class Board:
    def __init__(self, rows, columns):
        self.size = rows * columns
        self.no_rows = rows
        self.no_columns = columns
        self.squares = []
        for i in range(rows * columns):
            self.squares.append(0)

    def mark(self, index, player_id):
        self.squares[index] = player_id

    def get_rows(self):
        return nested_groups(self.squares, self.no_rows, self.no_columns, True)

    def get_columns(self):
        return nested_groups(self.squares, self.no_columns, self.no_rows, False)

    def get_diagonals(self):
        diags = [[],[]]
        if self.no_rows == self.no_columns:
            for i in range(self.no_rows):
                diags[0].append(self.get_columns()[i][i])
                diags[1].append(self.get_columns()[self.no_columns - 1 - i][i])
        else:
            diags = [[0],[0]]
        return diags

    def get_empty(self):
        empty = []
        for i in range(self.size):
            if self.squares[i] == 0:
                empty.append(i)
        return empty

class Move:
    def __init__(self, board):
        self.board = deepcopy(board)

    def play(self, player):
        return self.result(player.move(self.board), player)

    def result(self, square, player):
        self.board.mark(square, player.id)
        winner = self.check_win(self.board)
        if winner is None:
            if self.board.get_empty() == []:
                return 'tie'
            return None
        return winner

    def check_win(self, board):
        groups = [board.get_diagonals(), board.get_rows(), board.get_columns()]
        for group in groups:
            winner = self.find_winner(group)
            if winner is not None:
                return winner
        return None

    def find_winner(self, lst):
        for group in iter(lst):
            if 0 not in group and group[1:] == group[:-1]:
                return group[0] # mark in row is player.id of winner
        return None

class UI:
    def __init__(self, symbols):
        self.wall = '#'
        self.marks = symbols

    def draw(self, board):
        def row_edge():
            for i in range(board.no_columns * 4):
                print(self.wall, end='')
            print(self.wall)
        def row_label(row):
            for i in range(board.no_columns):
                label = str(coord_to_index(i, row, board.no_columns))
                if len(label) == 1:
                    label = label + '  '
                if len(label) == 2:
                    label = label + ' '
                print(self.wall + label, end='')
            print(self.wall)
        def row_center(row):
            for i in range(board.no_columns):
                print(self.wall + " " + self.marks[board.get_columns()[i][row]] + " ", end='')
            print(self.wall)
        def row_inside():
            for i in range(board.no_columns):
                print(self.wall + "   ", end='')
            print(self.wall)

        for row in range(board.no_rows):
            row_edge()
            row_label(row)
            row_center(row)
            row_inside()
        row_edge()

#class Player:
#    def __init__(self, name, symbol, identity, player_type):
#        self.name = name
#        self.symbol = symbol
#        self.id = identity
#        self.player_type = player_type
#
#    def move(self, board):
#        return self.player_type.choose_square(board)
#

class Human:
    def __init__(self, name, symbol, identity):
        self.name = name
        self.symbol = symbol
        self.id = identity

    def move(self, board):
        while True:
            try:
                val = int(input("Place mark in box number: "))
                if val not in board.get_empty():
                    print('Please input an available board piece')
                    print('Available spots: ' + str(board.get_empty()))
                    continue
                break
            except ValueError:
                print('Not a valid number!')
        return val

class Dummy:
    # The dummy class is simply a "dummy player" for the Analyzer class to input as a player placeholder
    def __init__(self, identity):
        self.id = identity

class Computer:
    def __init__(self, name, symbol, identity, opponent_id):
        self.name = name
        self.symbol = symbol
        self.id = identity
        self.opponent_id = opponent_id

    def move(self, board):
        print('Thinking...')
        player_self = Dummy(self.id)
        opponent = Dummy(self.opponent_id)
        decision = Analyzer(player_self, opponent, player_self.id, 0)
        return decision.best_move(board)['square']

class Analyzer:
    # Uses the minimax algorithm to decide best moves    
    def __init__(self, player_one, opponent, original_player_id, depth):
        self.player_one = player_one
        self.opponent = opponent
        self.original_player_id = original_player_id
        self.depth = depth
        
    def best_move(self, board):
        player = self.player_one
        moves_available = board.get_empty()
        move_scores = list(map(lambda square: {'square': square, 'score': self.get_score(square, board, player)}, moves_available))
        shuffle(move_scores) # so that the computer player doesn't always play the same move when there are other, equal options
        if player.id == self.original_player_id:
            best_moves = sorted(move_scores, key=itemgetter('score'), reverse=True)
        else:
            best_moves = sorted(move_scores, key=itemgetter('score'))
        return best_moves[0]

    def get_score(self, square, board, player):
        new_move = Move(board)
        outcome = new_move.result(square, player)
        if outcome is None:
            chooser = Analyzer(self.opponent, self.player_one, self.original_player_id, self.depth + 1)
            return chooser.best_move(new_move.board)['score']
        elif outcome == 'tie':
            score = 0
        elif outcome == self.original_player_id:
            score = 10
        else:
            score = -10
        return score - self.depth # subtract depth to find fastest path to winning

