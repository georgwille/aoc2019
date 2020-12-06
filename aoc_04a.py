range_start = 367479
range_stop = 893698


def isvalid(n):
    ns = str(n)
    if not len(ns) == 6:
        return False
    has_same = False
    for pos in range(len(ns) - 1):
        if ns[pos] > ns[pos + 1]:
            return False
        if ns[pos] == ns[pos + 1]:
            has_same = True
    return has_same


counter = 0

for i in range(range_start, range_stop + 1):
    if isvalid(i):
        counter += 1

print(counter)
