from helpers import clear_console, check_set, nested_groups
from itertools import cycle
from copy import deepcopy
from operator import itemgetter
from random import shuffle

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
                diags[0].append(self.columns()[i][i])
                diags[1].append(self.columns()[self.no_columns - 1 - i][i])
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
                val = int(input("\nPlace mark in box number: "))
                if val not in board.get_empty():
                    print('Please input an available board piece')
                    continue
                break
            except ValueError:
                print('Not a valid number!')
        return val
