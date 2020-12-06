# -*- coding: utf-8 -*-
"""
Created on Fri Dec 20 23:35:51 2019

@author: Georg
"""

import numpy as np
from copy import deepcopy

fin = open('input_24.txt')

eris = np.zeros((7,7), dtype = int)

for y,line in enumerate(fin,1):
    for x,char in enumerate(line,1):
        if char == '#':
            eris[y,x]=1
            
print(eris)

def nextgen(planet):
    temp = planet.copy()
    for y in range(1,planet.shape[0]-1):
        for x in range(1,planet.shape[1]-1):
            nbcount = planet[y+1,x]+planet[y-1,x]+planet[y,x+1]+planet[y,x-1]
            temp[y,x] = planet[y,x]
            if planet[y,x] == 1 and nbcount!=1:
                temp[y,x]=0
            elif planet[y,x] == 0 and (nbcount== 1 or nbcount ==2):
                temp[y,x] = 1

    for y in range(1,planet.shape[0]-1):
        for x in range(1,planet.shape[1]-1):
            planet[y,x] = temp[y,x]
            
def bdrating(planet):
    bd = 0
    for y in range(1,planet.shape[0]-1):
        for x in range(1,planet.shape[1]-1):
            ex = (x+(planet.shape[0]-2)*(y-1))-1
            print(x,y,ex, planet[y,x])
            bd += planet[y,x]*(2**ex)
    return bd
            
bdratings = set()

while True:
    bd = bdrating(eris)
    if bd not in bdratings:
        bdratings.add(bd)
        nextgen(eris)
    else:
        print(eris, bd)
        break

