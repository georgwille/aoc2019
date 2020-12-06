fin = open('input_05.txt')
temp = fin.readline()
fin.close()
temp = temp.split(',')
program_template = [int(x) for x in temp]

# program_template = [1002, 4, 3, 4, 33, 99]
# program_template = [1101, 100, -1, 4, 0]

ilength = {1: 4, 2: 4, 3: 2, 4: 2, 99: 1}


def pexec(p):

    pc = 0

    while True:
        # decode instruction
        opcode = p[pc] % 100
        modes = p[pc] // 100
        m1 = modes % 10
        modes = modes // 10
        m2 = modes % 10
        modes = modes // 10
        m3 = modes % 10
        # print(p[pc], opcode, m1, m2, m3)

        if opcode == 99:
            clean = True
            break

        elif opcode == 1:
            if m1 == 0:
                sum1 = p[p[pc + 1]]
            else:
                sum1 = p[pc + 1]
            if m2 == 0:
                sum2 = p[p[pc + 2]]
            else:
                sum2 = p[pc + 2]
            sum_ = sum1 + sum2
            if m3 == 0:
                p[p[pc + 3]] = sum_
            else:
                clean = False
                break

        elif opcode == 2:
            if m1 == 0:
                fac1 = p[p[pc + 1]]
            else:
                fac1 = p[pc + 1]
            if m2 == 0:
                fac2 = p[p[pc + 2]]
            else:
                fac2 = p[pc + 2]
            prod = fac1 * fac2
            if m3 == 0:
                p[p[pc + 3]] = prod
            else:
                clean = False
                break

        elif opcode == 3:
            inp = int(input('Input at location ' + str(pc) + ' : '))
            if m1 == 0:
                p[p[pc + 1]] = inp
            else:
                clean = False
                break

        elif opcode == 4:
            if m1 == 0:
                print(p[p[pc + 1]])
            elif m1 == 1:
                print(p[pc + 1])
            else:
                clean = False
                break

        else:
            clean = False
            break

        pc += ilength[opcode]

    return clean


p = program_template[:]
if pexec(p):
    print("Success")
else:
    print("Program has failed!")


quit()

for p1 in range(100):
    for p2 in range(100):
        p = program_template[:]
        p[1] = p1
        p[2] = p2
        pexec(p)
        if p[0] == 19690720:
            print(p1, p2)
