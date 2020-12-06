import numpy as np

fin = open('input_08.txt')
dstream = fin.readline().strip()
fin.close()

w = 25
h = 6

if len(dstream) % (w * h) != 0:
    print('Format mismatch')
    quit()

d = len(dstream) // (w * h)
print(d)

im = np.ndarray((h, w, d), dtype=int)

for k in range(d):
    for i in range(h):
        for j in range(w):
            im[i, j, k] = dstream[k * w * h + i * w + j]

print(im[:, :, 0])

zerocount = w * h + 1

for k in range(d):
    unique, counts = np.unique(im[:, :, k], return_counts=True)
    dcounts = dict(zip(unique, counts))
    # print(dcounts)
    if dcounts[0] < zerocount:
        zerocount = dcounts[0]
        print(k, zerocount, dcounts[1] * dcounts[2])
