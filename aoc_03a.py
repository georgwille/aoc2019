fin = open('input_03.txt')
t1 = fin.readline().strip().split(',')
t2 = fin.readline().strip().split(',')
fin.close()

# t1 = 'R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51'.strip().split(',')
# t2 = 'U98,R91,D20,R16,D67,R40,U7,R15,U6,R7'.strip().split(',')
# correct answer: 135

directions = {'U': (0, 1), 'D': (0, -1), 'L': (-1, 0), 'R': (1, 0)}


def path(t):
    coords = []
    x = 0
    y = 0
    for entry in t:
        dir_ = entry[0]
        delx, dely = directions[dir_]
        length = int(entry[1:])
        for c in range(length):
            x += delx
            y += dely
            coords.append((x, y))
    return coords


def mincrossing(path1, path2):
    s1 = set(path1)
    s2 = set(path2)
    scommon = s1.intersection(s2)
    min = 10**9
    for place in scommon:
        dist = abs(place[0]) + abs(place[1])
        if dist < min:
            min = dist
    return min


print(mincrossing(path(t1), path(t2)))
