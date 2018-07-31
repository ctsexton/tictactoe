from game import Game, Board, Square
from time import sleep

rows = 3
columns = 3

def main():
    print('\nWelcome to TIC TAC TOE!\n')
    game = Game(Board(rows, columns, Square, '$'))
    sleep(1)
    game.start()

if __name__ == "__main__":
    main()
