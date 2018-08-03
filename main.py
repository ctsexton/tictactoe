from library import Game, Board, Player, Human, Computer, UI
from helpers import clear_console

rows = 3
columns = 3

def main():
    print('\nWelcome to TIC TAC TOE!\n')
    name = input('Please enter your name: ')

    symbol = 'X'
    human = Player(name, symbol, 1, Human())
    computer = Player('HAL', 'O', 2, Computer())

    board = Board(rows, columns)
    players = [human, computer]

    game = Game(board, players)
    game.start()

if __name__ == "__main__":
    main()
