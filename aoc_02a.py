fin = open('input_02.txt')
_ = fin.readline()
fin.close()

_ = _.split(',')

program = [int(x) for x in _]

program[1] = 12

program[2] = 2

# program = [1,1,1,4,99,5,6,0,99]

print(program)

pcounter = 0

while True:
    if program[pcounter] == 99:
        clean = True
        break
    elif program[pcounter] == 1:
        program[program[pcounter + 3]] = program[program[pcounter + 1]
                                                 ] + program[program[pcounter + 2]]
    elif program[pcounter] == 2:
        program[program[pcounter + 3]] = program[program[pcounter + 1]
                                                 ] * program[program[pcounter + 2]]
    else:
        clean = False
        break
    pcounter += 4

print(program)
