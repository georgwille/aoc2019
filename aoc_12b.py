from copy import deepcopy
from sympy import ilcm

pos = [[-10, -10, -13],
       [5, 5, -9],
       [3, 8, -16],
       [1, 3, -3]]

vel = [[0, 0, 0],
       [0, 0, 0],
       [0, 0, 0],
       [0, 0, 0]]


def find_period(pos, vel, steps):
    # steps limits search range (upper bound)
    initial = (deepcopy(pos), deepcopy(vel))
    counter = 0
    for step in range(steps):
        for b, body in enumerate(pos):
            for partner in pos:
                for i in [0, 1, 2]:
                    if body[i] > partner[i]:
                        vel[b][i] -= 1
                    elif body[i] < partner[i]:
                        vel[b][i] += 1
        for b, body in enumerate(pos):
            for i in [0, 1, 2]:
                body[i] += vel[b][i]
        counter += 1
        if (pos, vel) == initial:
            return counter
    return 0  # if period > steps (upper bound)

# the coordinate axes are independent
# total period is the least common multiple
# of the period for each axis


def find_period_xyz(pos, vel, steps):
    period = [0, 0, 0]
    # isolate each axis...
    for c in [0, 1, 2]:
        cpos = []
        for body in pos:
            cpos_b = [0, 0, 0]
            cpos_b[c] = body[c]
            cpos.append(cpos_b)
        cvel = []
        for bodyv in vel:
            cvel_b = [0, 0, 0]
            cvel_b[c] = bodyv[c]
            cvel.append(cvel_b)
        # ...and find its period
        period[c] = find_period(cpos, cvel, steps)

    return ilcm(*period)  # sympy least common multiple


print(find_period_xyz(pos, vel, 10**6))
