# -*- coding: utf-8 -*-
"""
Created on Fri Dec 20 23:35:51 2019

@author: Georg
"""

from copy import deepcopy

fin = open('input_20.txt')
maze = []
for line in fin:
    l = []
    for char in line.strip('\n'):
        l.append(char)
    maze.append(l)


def print_maze(maze):
    for i, line in enumerate(maze):
        for char in line:
            print(char, end='')
        print(i)


def fill(maze):
    gates, rgates = findgates(maze)
    startx = gates['AA'][0][0]
    starty = gates['AA'][0][1]
    expanding = True
    t1 = deepcopy(maze)
    t2 = deepcopy(maze)
    t1[starty][startx] = '%'
    print_maze(t1)
    floodsteps = 0
    while expanding:
        floodsteps += 1
        print(floodsteps)
        expanding = False
        for y, line in enumerate(t1[2:-2], 2):
            for x, char in enumerate(line[2:-2], 2):
                if char in '.':
                    if t1[y][x + 1] == '%' or t1[y][x - 1] == '%' or t1[y + 1][x] == '%' or t1[y - 1][x] == '%':
                        t2[y][x] = '%'
                        expanding = True
                        if rgates.get((x, y), 'X') == 'ZZ':
                            print_maze(t2)
                            return floodsteps
                    if (x, y) in rgates:
                        door = rgates[(x, y)]
                        for jx, jy in gates[door]:
                            if t1[jy][jx] == '%':
                                t2[y][x] = '%'
                                expanding = True

        t1 = deepcopy(t2)

    print_maze(t1)
    return floodsteps


LETTERS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'


def findgates(maze):
    gates = {}
    rgates = {}
    for y, line in enumerate(maze[:-2]):
        for x, char in enumerate(line[:-2]):
            c1 = maze[y][x]
            c2 = maze[y + 1][x]
            c3 = maze[y + 2][x]

            if c1 in LETTERS and c2 in LETTERS and c3 == '.':
                rgates[(x, y + 2)] = c1 + c2
                if c1 + c2 in gates:
                    gates[c1 + c2].append((x, y + 2))
                else:
                    gates[c1 + c2] = [(x, y + 2)]

            if c2 in LETTERS and c3 in LETTERS and c1 == '.':
                rgates[(x, y)] = c2 + c3
                if c2 + c3 in gates:
                    gates[c2 + c3].append((x, y))
                else:
                    gates[c2 + c3] = [(x, y)]

            c1 = maze[y][x]
            c2 = maze[y][x + 1]
            c3 = maze[y][x + 2]

            if c1 in LETTERS and c2 in LETTERS and c3 == '.':
                rgates[(x + 2, y)] = c1 + c2
                if c1 + c2 in gates:
                    gates[c1 + c2].append((x + 2, y))
                else:
                    gates[c1 + c2] = [(x + 2, y)]

            if c2 in LETTERS and c3 in LETTERS and c1 == '.':
                rgates[(x, y)] = c2 + c3
                if c2 + c3 in gates:
                    gates[c2 + c3].append((x, y))
                else:
                    gates[c2 + c3] = [(x, y)]

    return gates, rgates


fill(maze)
