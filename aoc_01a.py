fin = open('input_01.txt')

sum = 0


def calcfuel(weight):
    addon = weight // 3 - 2
    if addon == 0:
        return 0
    else:
        return addon + weight(addon)


for line in fin:
    weight = int(line)
    fuel = calcfuel(weight)
    sum += fuel

print(sum)
