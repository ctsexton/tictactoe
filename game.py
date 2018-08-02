from helpers import is_valid_input, clear_console, check_set, coord_to_index
from itertools import cycle
from players import Human, Computer

class Board:
    def __init__(self, rows, columns, wall_symbol="#"):
        self.size = rows * columns
        self.nrows = rows
        self.ncolumns = columns
        self.squares = []
        self.wall = wall_symbol
        for i in range(columns):
            self.squares.append([])
            for j in range(rows):
                self.squares[i].append(0)

    def mark(self, x, y, player):
        self.squares[x][y] = player

    def rows(self):
        all_rows = []
        for index in range(self.nrows):
            all_rows.append([])
            for column in range(self.ncolumns):
                all_rows[index].append(self.squares[column][index])
        return all_rows

    def columns(self):
        return self.squares

    def diagonals(self):
        diags = [[],[]]
        if self.nrows == self.ncolumns:
            for i in range(self.nrows):
                diags[0].append(self.squares[i][i])
                diags[1].append(self.squares[self.ncolumns - 1 - i][i])
        else:
            diags = [[0],[0]]
        return diags

    def get_empty(self):
        empty = []
        for i in range(self.nrows):
            for j in range(self.ncolumns):
                if (self.squares[j][i] == 0):
                    empty.append(coord_to_index(j, i, self.nrows, self.ncolumns))
        return empty

    def draw(self):
        marks = [' ', 'X', 'O']
        def row_edge():
            for i in range(self.ncolumns * 4):
                print(self.wall, end='')
            print(self.wall)
        def row_inside():
            for i in range(self.ncolumns):
                print(self.wall + "   ", end='')
            print(self.wall)
        def row_center(row):
            for i in range(self.ncolumns):
                print(self.wall + " " + marks[self.squares[i][row]] + " ", end='')
            print(self.wall)

        for row in range(self.nrows):
            row_edge()
            row_inside()
            row_center(row)
            row_inside()
        row_edge()

class Game:
    def __init__(self, board, players):
        self.board = board
        self.players = cycle(players)

    def start(self):
        clear_console()
        self.board.draw()
        self.move(self.board, self.turn())

    def turn(self):
        next_player = next(self.players)
        print(next_player.name + ': ')
        return next_player

    def move(self, board, player):
        print(board.get_empty())
        comp = Computer()
        comp.choose_square(board)
        position = player.move(board)
        if position is None:
            self.move(board, player)
        else:
            board.mark(position.x, position.y, player.id)
            if not self.evaluate_board():
                clear_console()
                board.draw()
                self.move(board, self.turn())
            else:
                clear_console()
                board.draw()
                self.win(player)

    def evaluate_board(self):
        if check_set(self.board.columns()):
            return True
        if check_set(self.board.rows()):
            return True
        if check_set(self.board.diagonals()):
            return True
        return False

    def win(self, player):
        print("\n" + player.name + " WON!!!\n")

class Point:
    def __init__(self, index, rows, columns):
        self.x = index % columns
        self.y = index // columns
        self.number = index

    def coordinates(self):
        return [self.x, self.y]


class Player:
    def __init__(self, name, symbol, identity, player_type):
        self.name = name
        self.symbol = symbol
        self.id = identity
        self.player_type = player_type

    def move(self, board):
        selection = self.player_type.choose_square(board)
        return self.validate_square(board, selection)

    def validate_square(self, board, selection):
        if (is_valid_input(selection, 0, board.size)):
            position = Point(int(selection), len(board.rows()), len(board.columns()))
        else:
            print('Please input a number from 0 to ' + str(board.size - 1))
            return None
        if self.is_not_taken(board, position.x, position.y):
            return position
        else:
            print("Square taken!")
        return None

    def is_not_taken(self, board, x, y):
        if not board.squares[x][y] == 0:
            return False
        return True

