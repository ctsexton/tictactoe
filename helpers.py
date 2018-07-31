def is_Int(s):
    try: 
        int(s)
        return True
    except ValueError:
        return False

def is_valid_input(s, minimum, maximum):
    if not is_Int(s):
        return False
    if int(s) < minimum:
        return False
    if int(s) >= maximum:
        return False
    return True

def clear_console():
    print("\033[H\033[J")

def draw(board):
    def row_edge():
        for i in range(board.columns * 4):
            print(board.wall, end='')
        print(board.wall)
    def row_inside():
        for i in range(board.columns):
            print(board.wall + "   ", end='')
        print(board.wall)
    def row_center(row):
        for i in range(board.columns):
            print(board.wall + " " + board.squares[i][row].mark + " ", end='')
        print(board.wall)

    clear_console()

    for row in range(board.rows):
        row_edge()
        row_inside()
        row_center(row)
        row_inside()
    row_edge()

