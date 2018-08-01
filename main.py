from game import Game, Board, Player, Human

rows = 3
columns = 3

def main():
    print('\nWelcome to TIC TAC TOE!\n')
    name = input('Please enter your name: ')
    symbol = 'X'
    human = Player(name, symbol, 1, Human())
    computer = Player('HAL', 'O', 2, Human())
    game = Game(Board(rows, columns, '$'), [human, computer])
    game.start()

if __name__ == "__main__":
    main()
