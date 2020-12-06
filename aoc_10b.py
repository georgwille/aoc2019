from math import atan2, pi
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


def visible(coords):
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
    return d


max_count = 0

# (26, 28)

to_shoot = list(visible((26, 28)))

targets = []

for element in to_shoot:
    dx, dy = element
    angle = atan2(dx, -dy)
    if angle < 0:
        angle = angle + 2 * pi
    targets.append([angle, dx + 26, dy + 28])

targets.sort()

print(targets[199])

# this works only because the 200th target is less than
# one full rotation away (267 asteroids in view)
# the approach does _not_ produce a complete sequence of
# all asteroids in the order they are evaporated
