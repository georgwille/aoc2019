# -*- coding: utf-8 -*-
"""
Created on Sun Dec 15 14:21:16 2019

@author: Georg
"""

fin = open('input_15_check.txt')
temp = fin.readline().split(', ')
fin.close()

program_template = [int(x) for x in temp]

counter = -2

for p in program_template:
    d = [p//10, p%10]
    for i in d:
        counter += 1
        if i < 4:
            print('#',end='')
        else:
            print(' ',end='')
        if counter % 40 == 0:
            print('')