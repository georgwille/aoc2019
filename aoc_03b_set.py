import time
fin = open('input_03.txt')
t1 = fin.readline().strip().split(',')
t2 = fin.readline().strip().split(',')
fin.close()

# t1 = 'R8,U5,L5,D6'.strip().split(',')
# t2 = 'U7,R6,D4,L4'.strip().split(',')
# correct answer: 30

# t1 = 'R75,D30,R83,U83,L12,D49,R71,U7,L72'.strip().split(',')
# t2 = 'U62,R66,U55,R34,D71,R55,D58,R83'.strip().split(',')
# correct answer: 610

# t1 = 'R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51'.strip().split(',')
# t2 = 'U98,R91,D20,R16,D67,R40,U7,R15,U6,R7'.strip().split(',')
# correct answer: 410

directions = {'U': (0, 1), 'D': (0, -1), 'L': (-1, 0), 'R': (1, 0)}


def path(t):
    s = []
    coords = []
    coords_set = set()
    x = 0
    y = 0
    step = 0
    for entry in t:
        dir_ = entry[0]
        delx, dely = directions[dir_]
        length = int(entry[1:])
        for c in range(length):
            x += delx
            y += dely
            step += 1
            if (x, y) in coords_set:
                s.append(s[coords.index((x, y))])
            else:
                s.append(step)

            coords.append((x, y))
            coords_set.add((x, y))

    return coords, s


def mincrossing(path1, path2):
    track1 = path1[0]
    stepcount1 = path1[1]
    track2 = path2[0]
    stepcount2 = path2[1]

    d1 = {}
    for pos, count in zip(track1, stepcount1):
        d1[pos] = count
    d2 = {}
    for pos, count in zip(track2, stepcount2):
        d2[pos] = count

    s1 = set(track1)
    s2 = set(track2)
    scommon = s1.intersection(s2)
    min = 999999999999
    for place in scommon:
        dist = d1[place] + d2[place]
        if dist < min:
            min = dist
    return min


starttime = time.time()
print(mincrossing(path(t1), path(t2)))
print(time.time() - starttime)
