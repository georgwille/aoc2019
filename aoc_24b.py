# -*- coding: utf-8 -*-
"""
Created on Fri Dec 20 23:35:51 2019

@author: Georg
"""

import numpy as np
from copy import deepcopy

fin = open('input_24.txt')

eris = np.zeros((7,7,501), dtype = int)

for y,line in enumerate(fin,1):
    for x,char in enumerate(line,1):
        if char == '#':
            eris[y,x,250]=1
            
print(eris)

def nextgen(planet):
    temp = planet.copy()
    for l in range(1,500):
        for y in range(1,6):
            for x in range(1,6):
                if y == 1:
                    up = planet[2,3,l-1]
                elif y == 4 and x == 3:
                    up = planet[5,1:6,l+1].sum()
                else:
                    up = planet[y-1,x,l]
                if y == 5:
                    down = planet[4,3,l-1]
                elif y == 2 and x == 3:
                    down = planet[1,1:6,l+1].sum()
                else:
                    down = planet[y+1,x,l]
                if x == 1:
                    left = planet[3,2,l-1]
                elif x == 4 and y == 3:
                    left = planet[1:6,5,l+1].sum()
                else:
                    left = planet[y,x-1,l]
                if x == 5:
                    right = planet[3,4,l-1]
                elif x == 2 and y == 3:
                    right = planet[1:6,1,l+1].sum()
                else:
                    right = planet[y,x+1,l]
                
                nbcount = up+down+left+right
                temp[y,x,l] = planet[y,x,l]
                if planet[y,x,l] == 1 and nbcount!=1:
                    temp[y,x,l]=0
                elif planet[y,x,l] == 0 and (nbcount== 1 or nbcount ==2):
                    temp[y,x,l] = 1
                temp[3,3,l] = 0

    for l in range(1,500):
        for y in range(1,6):
            for x in range(1,6):
                planet[y,x,l] = temp[y,x,l]

genmax = 200

for i in range(genmax):
    nextgen(eris)

print(eris[1:6,1:6,1:501].sum())
