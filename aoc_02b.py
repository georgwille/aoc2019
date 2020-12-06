fin = open('input_02.txt')
temp = fin.readline()
fin.close()

temp = temp.split(',')

program_template = [int(x) for x in temp]


def pexec(p):

    pcounter = 0

    while True:
        if p[pcounter] == 99:
            break
        elif p[pcounter] == 1:
            p[p[pcounter + 3]] = p[p[pcounter + 1]
                                   ] + p[p[pcounter + 2]]
        elif p[pcounter] == 2:
            p[p[pcounter + 3]] = p[p[pcounter + 1]
                                   ] * p[p[pcounter + 2]]
        else:
            break
        pcounter += 4


for p1 in range(100):
    for p2 in range(100):
        p = program_template[:]
        p[1] = p1
        p[2] = p2
        pexec(p)
        if p[0] == 19690720:
            print(p1, p2)
