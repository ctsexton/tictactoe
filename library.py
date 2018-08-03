from helpers import clear_console, check_set, nested_groups, check_equal
from itertools import cycle
from copy import deepcopy
from operator import itemgetter
from random import shuffle

class Controller:
    def __init__(self, board, players):
        self.board = board
        self.ui = UI()
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
        game = Game(board)
        player = self.turn()
        result = game.play(player)
        clear_console()
        self.ui.draw(game.board)
        if result['score'] == 2:
            self.loop(game.board)
        elif result['score'] == 0:
            self.tie()
        else:
            self.win(player)

    def win(self, player):
        print("\n" + player.name + " WON!!!\n")

    def tie(self):
        print("\nIt was a tie!\n")

class Game:
    def __init__(self, board):
        self.board = deepcopy(board)

    def play(self, player):
        selected_square = player.move(self.board)
        return self.get_score(selected_square, player)

    def get_score(self, square, player):
        self.board.mark(square, player.id)
        score = self.score(self.board, player)
        return {'square': square, 'score': score}

    def score(self, board, player):
        winner = self.check_win(board)
        if winner is None:
            if board.get_empty() == []:
                return 0 # Tie
            return 2 # Incomplete
        if winner == player.id:
            return 1 # Win
        if winner != player.id:
            return -1 # Lose

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

class UI:
    def __init__(self):
        self.wall = '#'

    def draw(self, board):
        marks = [' ', 'X', 'O']
        def row_edge():
            for i in range(board.no_columns * 4):
                print(self.wall, end='')
            print(self.wall)
        def row_inside():
            for i in range(board.no_columns):
                print(self.wall + "   ", end='')
            print(self.wall)
        def row_center(row):
            for i in range(board.no_columns):
                print(self.wall + " " + marks[board.get_columns()[i][row]] + " ", end='')
            print(self.wall)

        for row in range(board.no_rows):
            row_edge()
            row_inside()
            row_center(row)
            row_inside()
        row_edge()

class Player:
    def __init__(self, name, symbol, identity, player_type):
        self.name = name
        self.symbol = symbol
        self.id = identity
        self.player_type = player_type

    def move(self, board):
        return self.player_type.choose_square(board)

class Human:
    def choose_square(self, board):
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

class Computer:
    def choose_square(self, board):
        return self.best_move(board, 2)['square']
        
    def best_move(self, board, player):
        moves_available = board.get_empty()
        move_scores = list(map(lambda square: self.get_score(square, board, player), moves_available))
        shuffle(move_scores)
        if player.id == 1:
            best_move = sorted(moves_available, key=itemgetter('score'), reverse=True)
        else:
            best_move = sorted(moves_available, key=itemgetter('score'))
        return best_move[0]

    def get_score(self, square, board, player):
        new_game = Game(board)
        score = new_game.get_score(square, player)
        if score == 2:
            new_player = self.switch_player(player)
            outcome = self.best_move(new_board, new_player)
            return {'square': square, 'score': outcome['score']}
        else:
            return {'square': square, 'score': score}
        
    def switch_player(self, player):
        if player == 1:
            return 2
        return 1

    def turn(self):
        next_player = next(self.players)
        print(next_player.name + ': ')
        return next_player

