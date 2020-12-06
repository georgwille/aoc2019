fin = open('input_06.txt')
# fin = open('test_06.txt')

tree = {}

# build tree

for line in fin:
    items = line.split(')')
    center = items[0]
    orbit = items[1].strip()
    if center in tree:
        tree[center].append(orbit)
    else:
        tree[center] = [orbit]
    if orbit not in tree:
        tree[orbit] = []

fin.close()

# insert undefined body counts

for k in tree:
    tree[k] = [tree[k], -1]

# print(tree)


def count_bodies_around(node):
    ''' recursive body count aroung node
    '''
    if tree[node][0] == []:
        tree[node][1] = 1
        return 1
    else:
        count = 1
        for subnode in tree[node][0]:
            count += count_bodies_around(subnode)
        tree[node][1] = count
        return count


print(count_bodies_around('COM'), "bodies around COM")

# print(tree)


def count_orbits_around(node):
    '''recursive orbit count around node
    '''
    count = 0
    for subnode in tree[node][0]:
        count += count_orbits_around(subnode)
    return count + tree[node][1] - 1


print(count_orbits_around('COM'), "orbits around COM")
