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

def check_equal(lst):
    return lst[1:] == lst[:-1]

def check_set(lst):
    for row in iter(lst):
        if 0 not in row and check_equal(row):
            return True
    return False

def draw(board):
    marks = [' ', 'X', 'O']
    def row_edge():
        for i in range(board.ncolumns * 4):
            print(board.wall, end='')
        print(board.wall)
    def row_inside():
        for i in range(board.ncolumns):
            print(board.wall + "   ", end='')
        print(board.wall)
    def row_center(row):
        for i in range(board.ncolumns):
            print(board.wall + " " + marks[board.squares[i][row]] + " ", end='')
        print(board.wall)

    clear_console()

    for row in range(board.nrows):
        row_edge()
        row_inside()
        row_center(row)
        row_inside()
    row_edge()

