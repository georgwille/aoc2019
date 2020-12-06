from itertools import permutations

fin = open('input_07.txt')
temp = fin.readline().split(',')
fin.close()

program_template = [int(x) for x in temp]
# program_template = [3, 26, 1001, 26, -4, 26, 3, 27, 1002, 27, 2, 27, 1, 27, 26,
#                     27, 4, 27, 1001, 28, -1, 28, 1005, 28, 6, 99, 0, 0, 5]
# program_template = [3, 52, 1001, 52, -5, 52, 3, 53, 1, 52, 56, 54, 1007, 54, 5, 55, 1005, 55, 26, 1001, 54,
#                     -5, 54, 1105, 1, 12, 1, 53, 54, 53, 1008, 54, 0, 55, 1001, 55, 1, 55, 2, 53, 55, 53, 4,
#                     53, 1001, 56, -1, 56, 1005, 56, 6, 99, 0, 0, 0, 0, 10]


def pexec(p, pc, in_queue, out_queue):

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

    while True:
        # decode instruction
        opcode = p[pc] % 100

        if opcode == 99:  # terminate
            return 'END', pc

        elif opcode == 1:  # add
            p[g_o(pc, 3)] = g_o(pc, 1) + g_o(pc, 2)
            pc += 4

        elif opcode == 2:  # multiply
            p[g_o(pc, 3)] = g_o(pc, 1) * g_o(pc, 2)
            pc += 4

        elif opcode == 3:  # input
            # inp = int(input('Input at location ' + str(pc) + ' : '))
            if in_queue == []:
                return 'WAIT', pc
            inp = in_queue.pop(0)
            p[p[pc + 1]] = inp
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

        else:  # unknown opcode
            return 'ERROR', pc


max_thrust = 0

for phases in permutations([5, 6, 7, 8, 9]):
    # programs for the amplifiers
    pA = program_template[:]
    pB = program_template[:]
    pC = program_template[:]
    pD = program_template[:]
    pE = program_template[:]

    # input queues (also target for output)
    qA = [phases[0], 0]
    qB = [phases[1]]
    qC = [phases[2]]
    qD = [phases[3]]
    qE = [phases[4]]

    # program counters
    pcA = 0
    pcB = 0
    pcC = 0
    pcD = 0
    pcE = 0

    # amplifier states
    stateA = 'WAIT'
    stateB = 'WAIT'
    stateC = 'WAIT'
    stateD = 'WAIT'
    stateE = 'WAIT'

    while True:
        # print('Before:', qA, qB, qC, qD, qE)
        if stateA == 'WAIT':
            stateA, pcA = pexec(pA, pcA, qA, qB)
        # print('A:', stateA, pcA, qA, qB)
        if stateB == 'WAIT':
            stateB, pcB = pexec(pB, pcB, qB, qC)
        # print('B:', stateB, pcB, qB, qC)
        if stateC == 'WAIT':
            stateC, pcC = pexec(pC, pcC, qC, qD)
        # print('C:', stateC, pcC, qC, qD)
        if stateD == 'WAIT':
            stateD, pcD = pexec(pD, pcD, qD, qE)
        # print('D:', stateD, pcD, qD, qE)
        if stateE == 'WAIT':
            stateE, pcE = pexec(pE, pcE, qE, qA)
        # print('E:', stateE, pcE, qE, qA)
        # print('After:', qA, qB, qC, qD, qE)
        # bla = input()
        if stateE == 'END':
            break

    if qA[0] > max_thrust:
        max_thrust = qA[0]

print(max_thrust)
