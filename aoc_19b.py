# -*- coding: utf-8 -*-

''' The complete Intcode computer
N. B. Someone wrote an intcode computer in intcode
https://www.reddit.com/r/adventofcode/comments/e7wml1/2019_intcode_computer_in_intcode/
'''

from os import system
import time

fin = open('input_19.txt')
temp = fin.readline().split(',')
fin.close()

program_template = [int(x) for x in temp]

# memory extension
program_template += [0] * 10000


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
        # print(pc)
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
    system('cls')
    char = {46: ' ', 35: '#', 94: '^', 60: '<',
            62: '>', 118: 'v', 0: '.', 1: '#'}
    for y, line in enumerate(canvas):
        for x, element in enumerate(line):
            if x == rx and y == ry:
                print('D', end='')
            else:
                print(char[element], end='')
        print('|', y)
    print('\n y:', ry, 'x:', rx)


def calib(cv):
    width = len(cv[1])
    height = len(cv)
    checksum = 0
    for y in range(1, height - 1):
        for x in range(1, width - 1):
            if cv[y][x] + cv[y - 1][x] + cv[y + 1][x] + cv[y][x - 1] + cv[y][x + 1] == 5 * 35:
                checksum += x * y
    return checksum


def run_once(cur_input):
    # computer initial state
    pA = program_template[:]
    qAin = cur_input
    qAout = []
    pcA = 0
    stateA = 'WAIT'
    rbaseA = 0

    # print(qAin)

    while True:
        if stateA == 'WAIT':
            stateA, pcA, rbaseA = pexec(pA, pcA, qAin, qAout, rbaseA)
        response = qAout.pop()
        if stateA == 'END':
            break

    return response


cv = [[-1 for x in range(50)] for y in range(50)]
xbeam = 0
shipfound = False
shipsize = 100

starttime = time.time()

for y in range(8, 4000):
    beamfound = False
    if shipfound:
        break
    for x in range(xbeam, 4000):
        ul = run_once([x, y])
        if ul == 1:
            if not beamfound:
                xbeam = x
            beamfound = True
            ur = run_once([x + shipsize - 1, y])
            if ur == 0:
                break
            ll = run_once([x, y + shipsize - 1])
            if ll == 1:
                print(x, y)
                shipfound = True
            if ur == 0:
                break

print(time.time() - starttime)
