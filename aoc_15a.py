''' The complete Intcode computer
N. B. Someone wrote an intcode computer in intcode
https://www.reddit.com/r/adventofcode/comments/e7wml1/2019_intcode_computer_in_intcode/
'''
from os import system


fin = open('input_15.txt')
temp = fin.readline().split(',')
fin.close()

program_template = [int(x) for x in temp]

# memory extension
program_template += [0] * 2000


def pexec(p, pc, in_queue, out_queue, rbase):

    def g_o(pc, opnum):  # get operand
        modes = p[pc] // 100
        m = [0, 0, 0, 0]
        m[1] = modes % 10
        modes = modes // 10
        m[2] = modes % 10
        modes = modes // 10
        m[3] = modes % 10

        if (opnum == 3):  # target address for write operations
            if m[3] == 0:
                return p[pc + opnum]
            else:
                return p[pc + opnum] + rbase

        if (p[pc] % 100 == 3):  # target address for input write
            if m[1] == 0:
                return p[pc + opnum]
            else:
                return p[pc + opnum] + rbase

        if m[opnum] == 0:  # positional, immediate, relative target value
            return p[p[pc + opnum]]
        elif m[opnum] == 1:
            return p[pc + opnum]
        elif m[opnum] == 2:
            return p[p[pc + opnum] + rbase]
        else:
            return None

    while True:
        # decode instruction
        opcode = p[pc] % 100

        if opcode == 99:  # terminate
            return 'END', pc, rbase

        elif opcode == 1:  # add
            p[g_o(pc, 3)] = g_o(pc, 1) + g_o(pc, 2)
            pc += 4

        elif opcode == 2:  # multiply
            p[g_o(pc, 3)] = g_o(pc, 1) * g_o(pc, 2)
            pc += 4

        elif opcode == 3:  # input
            if in_queue == []:
                return 'WAIT', pc, rbase
            inp = in_queue.pop(0)
            p[g_o(pc, 1)] = inp
            pc += 2

        elif opcode == 4:  # print
            out_queue.append(g_o(pc, 1))
            pc += 2

        elif opcode == 5:  # jump-if-true
            if g_o(pc, 1) != 0:
                pc = g_o(pc, 2)
            else:
                pc += 3

        elif opcode == 6:  # jump-if-false
            if g_o(pc, 1) == 0:
                pc = g_o(pc, 2)
            else:
                pc += 3

        elif opcode == 7:  # less than
            if g_o(pc, 1) < g_o(pc, 2):
                p[g_o(pc, 3)] = 1
            else:
                p[g_o(pc, 3)] = 0
            pc += 4

        elif opcode == 8:  # less than
            if g_o(pc, 1) == g_o(pc, 2):
                p[g_o(pc, 3)] = 1
            else:
                p[g_o(pc, 3)] = 0
            pc += 4

        elif opcode == 9:  # change relative base
            rbase += g_o(pc, 1)
            pc += 2

        else:  # unknown opcode
            return 'ERROR', pc, rbase


def print_canvas(canvas, ry, rx):
    # system('cls')
    char = {-1: ' ', 0: '.', 1: '#', 2: 'O'}
    for y, line in enumerate(canvas):
        for x, element in enumerate(line):
            if x == rx and y == ry:
                print('D', end='')
            else:
                print(char[element], end='')
        print('|')
    print('\n y:', ry, 'x:', rx)


# computer initial state
pA = program_template[:]
qAin = []
qAout = []
pcA = 0
stateA = 'WAIT'
rbaseA = 0

# canvas and robot position
width = 51
height = 51
cv = [[-1] * width for i in range(height)]  # coords in (y,x) order
r_xpos = width // 2
r_ypos = height // 2
cv[r_ypos][r_xpos] = 0
# -1-unknown, 0-free, 1-wall, 2-oxygen
dyx = {'n': (-1, 0), 'w': (0, -1), 's': (1, 0), 'e': (0, 1)}  # nwse
print_canvas(cv, r_ypos, r_xpos)
idir = {'n': 1, 'w': 3, 's': 2, 'e': 4}
stopsignal = False
init1 = 'sssssseennnneennnnnnnneennwwwwnneeeennwwnneeeenneeeeeennwwwwwwww'
init2 = 'nnwwsssswwsssswwsssssseesswwwwsswwsseesswwwwsseeeesswwwwsswwssww'
init3 = 'sseeeesssssswwnnnnwwsssswwnnnnwwwwwwsssswwnnnnnnnneennnnnnnnwwnn'
init4 = 'eeeeeennnnwwsswwnnwwnnnneesseenneennnnwwwwwwnnnnnneenneessssssee'
init5 = 'nnnneeeesswwsssseenneeeennwwnnnneeeesssseennnneeeesswwsssswwwwss'
init6 = 'eesssswwwwwwnnwwsssssswwsssssseesseesswwwwsssssswwwwww'
init = init1 + init2 + init3 + init4 + init5 + init6
print(len(init))
input()

while not stopsignal:
    if init == '':
        direction = input('nwse0:')
    else:
        direction = init
        init = ''
    for char in direction:
        if char == '0':
            stopsignal = True
        if char not in idir:
            continue
        qAin.append(idir[char])

        if stateA == 'WAIT':
            stateA, pcA, rbaseA = pexec(pA, pcA, qAin, qAout, rbaseA)
        response = qAout.pop()
        if response == 0:
            cv[r_ypos + dyx[char][0]][r_xpos + dyx[char][1]] = 1
        elif response == 1:
            cv[r_ypos + dyx[char][0]][r_xpos + dyx[char][1]] = 0
            r_ypos += dyx[char][0]
            r_xpos += dyx[char][1]
        elif response == 2:
            cv[r_ypos + dyx[char][0]][r_xpos + dyx[char][1]] = 2
            r_ypos += dyx[char][0]
            r_xpos += dyx[char][1]
    print_canvas(cv, r_ypos, r_xpos)
    if stateA == 'END':
        break

print_canvas(cv, r_ypos, r_xpos)

# This is all very manual and tedious, but automation would
# probably take even longer. First, explore the map, second
# find the shortest route to target. Then fill the maze with
# oxygen in the second part of the task. This last one I
# actually implemented.
