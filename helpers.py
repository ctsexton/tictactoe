def clear_console():
    print("\033[H\033[J")

def check_equal(lst):
    return lst[1:] == lst[:-1]

def check_set(lst):
    for row in iter(lst):
        if 0 not in row and check_equal(row):
            return True
    return False

def coord_to_index(x, y, rows, columns):
    return x % columns + y * rows

def index_to_coord(index, rows, columns):
    x = index % columns
    y = index // rows
    return {'x': x, 'y': y}

def nested_groups(original, no_groups, group_size, direction = True):
    groups = []
    i = 0
    for group in range(no_groups):
        groups.append([])
        for element in range(group_size):
            if direction == True:
                groups[group].append(original[coord_to_index(element, group, no_groups, group_size)])
            else:
                groups[group].append(original[coord_to_index(group, element, no_groups, group_size)])
    return groups
