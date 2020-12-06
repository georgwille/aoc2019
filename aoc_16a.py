import numpy as np


fin = open('input_16.txt')
_ = fin.readline().strip()
fin.close()

start = [int(char) for char in _]

start = start

start = np.asarray(start, dtype=int)

# print(start)


def multiplier(n, i):
    cycles = (n + 1) // i
    temp = [0] * i + [1] * i + [0] * i + [-1] * i
    temp = temp * cycles
    return temp[1:n + 1]


def fft(n):
    "Produce one iteration of 'fft'"
    l = len(n)
    answer = np.zeros((l))
    for i in range(l):
        m = multiplier(l, i + 1)
        p = sum(m * n)
        answer[i] = abs(p) % 10
    return answer


phases = 100
signal = start

for i in range(phases):
    signal = fft(signal)

print(signal[:8])
