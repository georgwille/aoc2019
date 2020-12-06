# -*- coding: utf-8 -*-
"""
Created on Fri Dec 20 23:35:51 2019

@author: Georg
"""

from copy import deepcopy

fin = open('input_20t3.txt')
level = []
for line in fin:
    l = []
    for char in line.strip('\n'):
        l.append(char)
    level.append(l)

fin.close()

VLEVELNO = 10  # default number of levels when printing
LEVELNO = 2

maze = [deepcopy(level), deepcopy(level)]

YSIZE = len(maze[0])
XSIZE = len(maze[0][0])

print('YSIZE {}, XSIZE {}'.format(YSIZE, XSIZE))


def print_maze(maze, levels=None, flood=None):
    if levels == None:
        levels = range(VLEVELNO)
    for l in range(VLEVELNO):
        if l not in levels:
            continue
        else:
            print('Level', l)
            if l == 0:
                level = maze[0]
            else:
                level = maze[1]
        for y, line in enumerate(level):
            for x, char in enumerate(line):
                if flood == None:
                    print(char, end='')
                else:
                    if (l, y, x) in flood:
                        print('o', end='')
                    else:
                        print(char, end='')
            print(y)


def fill(maze):
    igates, ogates, gates = findgates(maze)
    tip = set()  # tip is a set of flooded tiles at the flood front,
                 # will be checked for floodable neighbors next
    tip.add((0, gates['AA'][0][0], gates['AA'][0][1]))
    flood = set()  # list of already flooded coordinates (level, y, x)
    flood.add((0, gates['AA'][0][0], gates['AA'][0][1]))
    expanding = True
    floodsteps = 0

    # preparing the levels, i. e. blocking AA/ZZ in all levels but 0
    # blocking all other gates in level 0
    # this saves lots of testing for edge cases in the flooding phase

    for gate in ogates:
        y1, x1 = gate
        gname = ogates[gate][1]
        if gname not in ['AA', 'ZZ']:
            maze[0][y1][x1] = '#'
        else:
            maze[1][y1][x1] = '#'

    while expanding:
        floodsteps += 1
        nextround = set()  # those will go into 'tip' at the end of the loop
        print('Steps:', floodsteps, '  Tips:', len(tip))
        expanding = False
        # print_maze(maze,[0,1], flood)
        # input('Enter')
        # print(tip)
        for l, y, x in tip:

            # check if _current_ position is a gate
            # if so, spill to appropriate level
            if (y, x) in ogates and floodsteps > 1:
                # the 'floodsteps>1' is required or it will flood backwards
                # from AA on the first round
                if ogates[(y, x)][1] == 'ZZ':
                    print('Exit found')
                    return floodsteps - 1, flood
                flood.add((l - 1, ogates[(y, x)][0][0], ogates[(y, x)][0][1]))
                nextround.add(
                    (l - 1, ogates[(y, x)][0][0], ogates[(y, x)][0][1]))
                expanding = True

            if (y, x) in igates:
                flood.add((l + 1, igates[(y, x)][0][0], igates[(y, x)][0][1]))
                nextround.add(
                    (l + 1, igates[(y, x)][0][0], igates[(y, x)][0][1]))
                expanding = True

            # check 'plain' neighbors on same level
            for dy, dx in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                newy, newx = y + dy, x + dx
                if l > 0:
                    reql = 1
                else:
                    reql = 0
                if maze[reql][newy][newx] == '.' and (l, newy, newx) not in flood:
                    flood.add((l, newy, newx))
                    nextround.add((l, newy, newx))
                    expanding = True

        tip = deepcopy(nextround)

    return floodsteps, flood


LETTERS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'


def findgates(maze):
    # this tedious mess is due to the labeling scheme of the gates
    # but it needs to be run only once

    # all gate coordinates in (y,x) order
    igates = {}  # inner gates lead to level +1
    ogates = {}  # outer gates lead to level -1

    gates = {}

    level0 = maze[0]

    for y, line in enumerate(level0[:-2]):
        for x, char in enumerate(line[:-2]):
            c1 = level0[y][x]
            c2 = level0[y + 1][x]
            c3 = level0[y + 2][x]

            if c1 in LETTERS and c2 in LETTERS and c3 == '.':
                if c1 + c2 in gates:
                    gates[c1 + c2].append((y + 2, x))
                else:
                    gates[c1 + c2] = [(y + 2, x)]

            if c2 in LETTERS and c3 in LETTERS and c1 == '.':
                if c2 + c3 in gates:
                    gates[c2 + c3].append((y, x))
                else:
                    gates[c2 + c3] = [(y, x)]

            c1 = level0[y][x]
            c2 = level0[y][x + 1]
            c3 = level0[y][x + 2]

            if c1 in LETTERS and c2 in LETTERS and c3 == '.':
                if c1 + c2 in gates:
                    gates[c1 + c2].append((y, x + 2))
                else:
                    gates[c1 + c2] = [(y, x + 2)]

            if c2 in LETTERS and c3 in LETTERS and c1 == '.':
                if c2 + c3 in gates:
                    gates[c2 + c3].append((y, x))
                else:
                    gates[c2 + c3] = [(y, x)]

    for name in gates:
        if name in ['AA', 'ZZ']:
            ogates[gates[name][0]] = (gates[name][0], name)
            continue
        pair1, pair2 = gates[name]
        # print(name, gates[name], pair1, pair2)
        y, x = pair1
        if y == 2 or y == YSIZE - 3 or x == 2 or x == XSIZE - 3:
            ogates[pair1] = (pair2, name)
            igates[pair2] = (pair1, name)
        else:
            ogates[pair2] = (pair1, name)
            igates[pair1] = (pair2, name)

    return igates, ogates, gates


floodsteps, flood = fill(maze)
print(floodsteps)
