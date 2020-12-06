from sympy import gcd

fin = open('input_10.txt')
# fin = open('test_10.txt')

roids = []

for y, line in enumerate(fin):
    for x, char in enumerate(line.strip()):
        if char == '#':
            roids.append((x, y))

fin.close()
# print(roids)


def count_visible(coords):
    center_x, center_y = coords
    d = set()  # lines of sight (slope as denominator, divisor)
    for roid in roids:
        if center_x == roid[0] and center_y == roid[1]:
            continue
        if center_x == roid[0]:
            if roid[1] < center_y:
                d.add((-1, 0))
            else:
                d.add((1, 0))
        elif center_y == roid[1]:
            if roid[0] < center_x:
                d.add((0, -1))
            else:
                d.add((0, 1))
        else:
            xdiff = roid[0] - center_x
            ydiff = roid[1] - center_y
            this_gcd = gcd(xdiff, ydiff)
            d.add((xdiff // this_gcd, ydiff // this_gcd))
    return len(d)


max_count = 0

for roid in roids:
    count = count_visible(roid)
    if count > max_count:
        max_count = count
        max_roid = roid

print(max_roid, max_count)
