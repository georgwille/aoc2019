''' The complete Intcode computer
N. B. Someone wrote an intcode computer in intcode
https://www.reddit.com/r/adventofcode/comments/e7wml1/2019_intcode_computer_in_intcode/
'''
import os

fin = open('input_13x.txt')
temp = fin.readline().split(',')
fin.close()

program_template = [int(x) for x in temp]
# program_template = [109, 1, 204, -1, 1001, 100,
#                     1, 100, 1008, 100, 16, 101, 1006, 101, 0, 99]
# program_template = [1102, 34915192, 34915192, 7, 4, 7, 99, 0]
# program_template = [104, 1125899906842624, 99]

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
            # inp = int(input('Input at location ' + str(pc) + ' : '))
            if in_queue == []:
                return 'WAIT', pc, rbase
            inp = in_queue.pop(0)
            p[g_o(pc, 1)] = inp
            pc += 2

        elif opcode == 4:  # print
            # print(g_o(pc, 1))
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

        elif opcode == 8:  # equal
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


def printscr(screenstate):
    os.system('cls')
    width = max(screenstate[::3]) + 1
    height = max(screenstate[1::3]) + 1
    segment = 'undefined'
    screen = [[0] * width for i in range(height)]  # coords in (y,x)
    d = {0: ' ', 1: '#', 2: '=', 3: '-', 4: 'o'}
    for x, y, c in zip(*[iter(screenstate)] * 3):
        if x == -1 and y == 0:
            segment = c
            continue
        else:
            # print(y, x, c)
            screen[y][x] = d[c]
    for y in range(height):
        for x in range(width):
            print(screen[y][x], end='')
        print()
    print("Score: ", segment)


pA = program_template[:]
pA[0] = 2  # infinite quarters
qAin = []
qAout = []
pcA = 0
stateA = 'WAIT'
rbaseA = 0

while True:
    if stateA == 'WAIT':
        stateA, pcA, rbaseA = pexec(pA, pcA, qAin, qAout, rbaseA)
        printscr(qAout)
        # j = input('left(a)-neutral(s)-right(d)')
        j = 's'
        if j == 'a':
            qAin.append(-1)
        elif j == 'd':
            qAin.append(1)
        else:
            qAin.append(0)
    if stateA == 'END':
        break

# print(qAout)
