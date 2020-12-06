range_start = 367479
range_stop = 893698


def isvalid(n):
    ns = str(n)
    if not len(ns) == 6:
        return False
    lstretch = 1
    has_pair = False
    for pos in range(len(ns) - 1):
        if ns[pos] > ns[pos + 1]:
            return False
        if ns[pos] == ns[pos + 1]:
            lstretch += 1
            if (lstretch == 2) and (pos == 4):
                has_pair = True
        else:
            if lstretch == 2:
                has_pair = True
            lstretch = 1

    return has_pair


counter = 0

for i in range(range_start, range_stop + 1):
    if isvalid(i):
        print(i)
        counter += 1

print(counter)
