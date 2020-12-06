# ignore all the complications
# the required answer is in a range of the signal field
# that has only the trailing +1 chain of matrix elements
# this makes the calculation much easier, as all the
# leading digits up to this point can be safely ignored!

import numpy as np
# from numba import njit
import time

fin = open('input_16.txt')
_ = fin.readline().strip()
fin.close()

# _ = '03036732577212944063491565474664'

start = [int(char) for char in _]

mpos = int(_[:7])

print(mpos)

start = start[:] * 10000

start = start[mpos:]  # cut the leading junk part!

signal = np.asarray(start, dtype=int)
slen = len(signal)

print(signal)


phases = 100
temp = signal.copy()

starttime = time.time()

for i in range(phases):
    print(i)
    temp[-1] = signal[-1]
    for p in range(slen - 2, -1, -1):
        temp[p] = abs(temp[p + 1] + signal[p]) % 10
    signal = temp.copy()

    # print(signal)

print(signal[:8])
print(time.time() - starttime)
