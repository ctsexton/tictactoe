from library import Controller, Board, Player, Human, UI
from helpers import clear_console

rows = 3
columns = 3

def main():
    print('\nWelcome to TIC TAC TOE!\n')
    name = input('Please enter your name: ')

    symbol = 'X'
    human = Player(name, symbol, 1, Human())
    computer = Player('HAL', 'O', 2, Human())

    board = Board(rows, columns)
    players = [human, computer]

    control = Controller(board, players)
    control.start()

if __name__ == "__main__":
    main()
