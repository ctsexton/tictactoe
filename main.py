from library import Game, Board, Human, Computer
from helpers import clear_console

rows = 3
columns = 3

def main():
    print('\nWelcome to TIC TAC TOE!\n')
    name = input('Please enter your name: ')

    player_one_id = 1
    player_two_id = 2

    # Swap the commenting on the following two lines to pit computer against computer
    player_one = Human(name, 'X', player_one_id)
    #player_one = Computer(name, 'X', player_one_id, player_two_id)

    player_two = Computer('HAL', 'O', player_two_id, player_one_id)
    players = [player_one, player_two]

    board = Board(rows, columns)
    game = Game(board, players)
    game.start()

if __name__ == "__main__":
    main()
