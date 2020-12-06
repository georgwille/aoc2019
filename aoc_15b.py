from os import system
from copy import deepcopy

fin = open('aoc_15_maze.txt')
cv = []
for line in fin:
    thisline = []
    for char in line.strip():
        if char == '#':
            thisline.append(1)
        elif char == '.':
            thisline.append(0)
        elif char == 'O':
            thisline.append(2)
    cv.append(thisline)

fin.close()


def print_canvas(canvas):
    system('cls')
    char = {-1: ' ', 0: '.', 1: '#', 2: 'O'}
    for line in canvas:
        for element in line:
            print(char[element], end='')
        print('|')
    print('\n')


def o_around(cv, y, x):
    if cv[y - 1][x] == 2:
        return True
    if cv[y + 1][x] == 2:
        return True
    if cv[y][x - 1] == 2:
        return True
    if cv[y][x + 1] == 2:
        return True
    return False


print_canvas(cv)

stepcount = 0
filling = True

while filling:
    filling = False
    tcv = deepcopy(cv)
    for y, line in enumerate(cv[1:-1], 1):
        for x, char in enumerate(line[1:-1], 1):
            if cv[y][x] == 0 and o_around(cv, y, x):
                tcv[y][x] = 2
                filling = True
    if filling:
        stepcount += 1
    cv = deepcopy(tcv)
    print_canvas(cv)
    print(stepcount)
    # if input() == 'q':
    #     break

print(stepcount)
