fin = open('input_14.txt')
rx = {}  # reactions {'FUEL':[1, [('ABC',3), ('DEF',5)]]}
# rx[substance][0] = amount substance produced
# rx[substance][1] = list of (reactant, #) pairs

store = {}  # current store of leftover stuff

for line in fin:
    educts, product = line.strip().split('=>')
    p_amount, p_name = product.split()[0], product.split()[1]
    rx[p_name] = [int(p_amount), []]
    for educt in educts.split(','):
        e_amount, e_name = educt.split()[0], educt.split()[1]
        rx[p_name][1].append((int(e_amount), e_name))

# print(rx)


def ore_for(substance, req_amount):
    if substance == 'ORE':
        return req_amount
    if substance not in store:
        store[substance] = 0

    to_produce = req_amount - store[substance]
    cycles = (to_produce-1) // rx[substance][0] + 1
    store[substance] = cycles * rx[substance][0] - to_produce
    ore = 0
    for e_amount, educt in rx[substance][1]:
        # print(runfactor, '*', e_amount, 'of', educt)
        ore += ore_for(educt, cycles * e_amount)
    return ore


print(ore_for('FUEL', 1))
