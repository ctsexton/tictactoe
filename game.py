from helpers import is_valid_input, clear_console, draw

class Point:
    def __init__(self, index, rows, columns):
        self.x = index % columns
        self.y = index // columns
        self.number = index

    def coordinates(self):
        return [self.x, self.y]

class Square:
    def __init__(self, mark=" "):
        self.mark = mark
    def check(self, symbol):
        if (symbol == 'X' or symbol == 'O'):
            self.mark = symbol

class Board:
    def __init__(self, rows, columns, piece, wall_symbol="#"):
        self.size = rows * columns
        self.rows = rows
        self.columns = columns
        self.squares = []
        self.wall = wall_symbol
        for i in range(columns):
            self.squares.append([])
            for j in range(rows):
                self.squares[i].append(piece())

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
            board.squares[position.x][position.y].check('X')
            if not self.evaluate_board():
                draw(board)
                self.move(board)
            else:
                self.win()

    def select_square(self):
        box_number = input('Place mark in box: ')
        if (is_valid_input(box_number, 0, self.board.size)):
            position = Point(int(box_number), self.board.rows, self.board.columns)
        else:
            print('Please input a number from 0 to ' + str(self.board.size - 1))
            return None
        if self.is_not_taken(position.x, position.y):
            return position
        else:
            print("Square taken!")
        return None

    def is_not_taken(self, x, y):
        if not self.board.squares[x][y].mark == " ":
            return False
        return True

    def evaluate_board(self):
        return False

    def win(self):
        clear_console()
        print("YOU WON!!!")
