''' The complete Intcode computer
N. B. Someone wrote an intcode computer in intcode
https://www.reddit.com/r/adventofcode/comments/e7wml1/2019_intcode_computer_in_intcode/
'''

fin = open('input_11.txt')
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


def print_canvas(canvas):
    char = {-1: ' ', 0: '.', 1: '#'}
    for line in canvas:
        for element in line:
            print(char[element], end='')
        print('')
    print('\n')


max_thrust = 0

# computer initial state
pA = program_template[:]
qAin = []
qAout = []
pcA = 0
stateA = 'WAIT'
rbaseA = 0

# canvas and robot position
width = 200
height = 200
cv = [[-1] * width for i in range(height)]  # coords in (y,x) order
r_xpos = width // 2
r_ypos = height // 2
point_to = 0  # 0 up, 1 left, 2 down, 3 right
dyx = [(-1, 0), (0, -1), (1, 0), (0, 1)]
paintcount = 0
print_canvas(cv)

while True:
    if cv[r_ypos][r_xpos] < 1:
        qAin.append(0)
    else:
        qAin.append(1)

    if stateA == 'WAIT':
        stateA, pcA, rbaseA = pexec(pA, pcA, qAin, qAout, rbaseA)
    if qAout:
        if cv[r_ypos][r_xpos] == -1:
            paintcount += 1
        if qAout[0] == 1:
            cv[r_ypos][r_xpos] = 1
        if qAout[0] == 0:
            cv[r_ypos][r_xpos] = 0
        if qAout[1] == 0:
            point_to = (point_to - 1) % 4
        if qAout[1] == 1:
            point_to = (point_to + 1) % 4
        dy, dx = dyx[point_to]
        r_xpos += dx
        r_ypos += dy
        qAout = []
    # print_canvas(cv)
    if stateA == 'END':
        break

print(paintcount)
