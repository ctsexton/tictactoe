from helpers import is_valid_input, clear_console, draw, check_set

class Point:
    def __init__(self, index, rows, columns):
        self.x = index % columns
        self.y = index // columns
        self.number = index

    def coordinates(self):
        return [self.x, self.y]

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

class Game:
    def __init__(self, board):
        self.board = board

    def start(self):
        draw(self.board)
        self.move(self.board)

    def move(self, board):
        position = self.select_square()
        if position is None:
            self.move(board)
        else:
            board.mark(position.x, position.y, 1)
            if not self.evaluate_board():
                draw(board)
                self.move(board)
            else:
                draw(board)
                self.win()

    def select_square(self):
        box_number = input('\nPlace mark in box: ')
        if (is_valid_input(box_number, 0, self.board.size)):
            position = Point(int(box_number), self.board.nrows, self.board.ncolumns)
        else:
            print('Please input a number from 0 to ' + str(self.board.size - 1))
            return None
        if self.is_not_taken(position.x, position.y):
            return position
        else:
            print("Square taken!")
        return None

    def is_not_taken(self, x, y):
        if not self.board.squares[x][y] == 0:
            return False
        return True

    def evaluate_board(self):
        if check_set(self.board.columns()):
            return True
        if check_set(self.board.rows()):
            return True
        if check_set(self.board.diagonals()):
            return True
        return False

    def win(self):
        print("\nYOU WON!!!\n")

class Player:
    def __init__(self, name, symbol, identity):
        self.name = name
        self.symbol = symbol
        self.id = identity
