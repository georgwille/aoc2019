from itertools import permutations

fin = open('input_07.txt')
temp = fin.readline().split(',')
fin.close()

program_template = [int(x) for x in temp]


def g_o(pc, opnum):  # get operand
    modes = p[pc] // 100
    m = [0, 0, 0, 0]
    m[1] = modes % 10
    modes = modes // 10
    m[2] = modes % 10
    modes = modes // 10
    m[3] = modes % 10

    if opnum == 3:  # target address for write operations
        return p[pc + opnum]

    if m[opnum] == 0:  # immediate or positional input values
        return p[p[pc + opnum]]
    else:
        return p[pc + opnum]


def pexec(p, inputs):

    pc = 0
    inputpointer = 0
    output = []

    while True:
        # decode instruction
        opcode = p[pc] % 100

        if opcode == 99:  # terminate
            clean = True
            break

        elif opcode == 1:  # add
            p[g_o(pc, 3)] = g_o(pc, 1) + g_o(pc, 2)
            pc += 4

        elif opcode == 2:  # multiply
            p[g_o(pc, 3)] = g_o(pc, 1) * g_o(pc, 2)
            pc += 4

        elif opcode == 3:  # input
            # inp = int(input('Input at location ' + str(pc) + ' : '))
            inp = inputs[inputpointer]
            inputpointer += 1
            p[p[pc + 1]] = inp
            pc += 2

        elif opcode == 4:  # print
            print(g_o(pc, 1))
            output.append(g_o(pc, 1))
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

        else:  # unknown opcode
            clean = False
            break

    return clean, output


max_thrust = 0

for phases in permutations([0, 1, 2, 3, 4]):
    p = program_template[:]
    ampA = pexec(p, [phases[0], 0])[1][0]
    p = program_template[:]
    ampB = pexec(p, [phases[1], ampA])[1][0]
    p = program_template[:]
    ampC = pexec(p, [phases[2], ampB])[1][0]
    p = program_template[:]
    ampD = pexec(p, [phases[3], ampC])[1][0]
    p = program_template[:]
    ampE = pexec(p, [phases[4], ampD])[1][0]
    if ampE > max_thrust:
        max_thrust = ampE

print(max_thrust)
