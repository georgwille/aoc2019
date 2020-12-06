pos = [[-10, -10, -13],
       [5, 5, -9],
       [3, 8, -16],
       [1, 3, -3]]

vel = [[0, 0, 0],
       [0, 0, 0],
       [0, 0, 0],
       [0, 0, 0]]


def update(pos, vel, steps):
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
    return pos, vel


def energy(pos, vel):
    e = 0
    for body, bodyv in zip(pos, vel):
        epot = 0
        ekin = 0
        for _ in body:
            epot += abs(_)

        for _ in bodyv:
            ekin += abs(_)
        e += epot * ekin

    return e


print(update(pos, vel, 1000))
print(energy(pos, vel))
