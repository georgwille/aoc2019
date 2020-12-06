fin = open('input_06.txt')
# fin = open('test_06.txt')

tree = {}

# build tree
# list of direct children
# one parent

for line in fin:
    center, orbit = line.strip().split(')')
    if center in tree:
        tree[center][0].append(orbit)
    else:
        tree[center] = [[orbit], '']
    if orbit in tree:
        tree[orbit][1] = center
    else:
        tree[orbit] = [[], center]

fin.close()

print(tree)


def path_to_root(node, root='COM'):
    path = [node]
    while True:
        parent = tree[node][1]
        if parent in tree:
            path.append(parent)
        else:
            return (path, False)
        if parent == root:
            return path
        node = parent


def path_from_a_to_b(node1, node2, root='COM'):
    path1 = path_to_root(node1, root)
    path2 = path_to_root(node2, root)
    while path1[-1] == path2[-1]:
        path1.pop()
        path2.pop()
    return len(path1) + len(path2) - 2


print(path_to_root('YOU'), 'is the path from you to COM')
print(path_to_root('SAN'), 'is the path from Santa to COM')

print(path_from_a_to_b('YOU', 'SAN'), 'steps from you to Santa')
