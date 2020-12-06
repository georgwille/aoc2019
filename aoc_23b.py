# -*- coding: utf-8 -*-

''' The complete Intcode computer
N. B. Someone wrote an intcode computer in intcode
https://www.reddit.com/r/adventofcode/comments/e7wml1/2019_intcode_computer_in_intcode/
'''

from os import system
import time

fin = open('input_23.txt')
temp = fin.readline().split(',')
fin.close()

program_template = [int(x) for x in temp]

# memory extension
program_template += [0] * 10000

class IntcodeComputer():
    ''' The Intcode computer
    Initializes with program
    Has attributes
      p:         program
      pc:        program cursor (address of next instruction)
      in_queue:  waiting inputs
      self.out_queue: outputs produced
      rbase:     current base for relative addressing
      state:     current state (INIT, WAIT, END, ERROR)
      
    Has methods
      run: run execution until return
    '''
      
    
    def __init__(self, program):
        self.p = program[:]
        self.pc = 0 # programcursor
        self.in_queue = []
        self.out_queue = []
        self.rbase = 0 # relative address base
        self.state = 'INIT'

    def run(self):
        if self.state in ['ERROR','END']:
            print('Not in a runnable state')
            return
    
        def g_o(opnum):  # get operand
            modes = self.p[self.pc] // 100
            m = [0, 0, 0, 0]
            m[1] = modes % 10
            modes = modes // 10
            m[2] = modes % 10
            modes = modes // 10
            m[3] = modes % 10
    
            if (opnum == 3):  # target address for write operations
                if m[3] == 0:
                    return self.p[self.pc + opnum]
                else:
                    return self.p[self.pc + opnum] + self.rbase
    
            if (self.p[self.pc] % 100 == 3):  # target address for input write
                if m[1] == 0:
                    return self.p[self.pc + opnum]
                else:
                    return self.p[self.pc + opnum] + self.rbase
    
            if m[opnum] == 0:  # positional, immediate, relative target value
                return self.p[self.p[self.pc + opnum]]
            elif m[opnum] == 1:
                return self.p[self.pc + opnum]
            elif m[opnum] == 2:
                return self.p[self.p[self.pc + opnum] + self.rbase]
            else:
                return None
    
        while True:
            # decode instruction
            # print(self.pc)
            opcode = self.p[self.pc] % 100
    
            if opcode == 99:  # terminate
                self.state = 'END'
                return
    
            elif opcode == 1:  # add
                self.p[g_o(3)] = g_o(1) + g_o(2)
                self.pc += 4
    
            elif opcode == 2:  # multiply
                self.p[g_o(3)] = g_o(1) * g_o(2)
                self.pc += 4
    
            elif opcode == 3:  # input
                if self.in_queue == []:
                    self.state = 'WAIT'
                    return
                inp = self.in_queue.pop(0)
                self.p[g_o(1)] = inp
                self.pc += 2
    
            elif opcode == 4:  # print
                self.out_queue.append(g_o(1))
                self.pc += 2
    
            elif opcode == 5:  # jump-if-true
                if g_o(1) != 0:
                    self.pc = g_o(2)
                else:
                    self.pc += 3
    
            elif opcode == 6:  # jump-if-false
                if g_o(1) == 0:
                    self.pc = g_o(2)
                else:
                    self.pc += 3
    
            elif opcode == 7:  # less than
                if g_o(1) < g_o(2):
                    self.p[g_o(3)] = 1
                else:
                    self.p[g_o(3)] = 0
                self.pc += 4
    
            elif opcode == 8:  # less than
                if g_o(1) == g_o(2):
                    self.p[g_o(3)] = 1
                else:
                    self.p[g_o(3)] = 0
                self.pc += 4
    
            elif opcode == 9:  # change relative base
                self.rbase += g_o(1)
                self.pc += 2
    
            else:  # unknown opcode
                self.state = 'ERROR'
                return



# init network

netc = []
for i in range(50):
    netc.append(IntcodeComputer(program_template))
    netc[i].in_queue.append(i) # assign address
    netc[i].run()
    # print(netc[i].out_queue)
    
# main loop

print('Network start')
y1 = -999

while True:
    # check all output queues, put packets in input queues
    net_idle = True
    for i in range(50):        
        while len(netc[i].out_queue) > 0:
            address = netc[i].out_queue.pop(0)
            x = netc[i].out_queue.pop(0)
            y = netc[i].out_queue.pop(0)
            if address == 255:
                natx = x
                naty = y
                continue
            netc[address].in_queue.extend((x,y))
        if netc[i].in_queue == []:
            netc[i].in_queue.append(-1)
        netc[i].run()
        if netc[i].out_queue:
            net_idle = False
    if net_idle:
        netc[0].in_queue.extend((x,y))
        net_idle = False
        print('NAT activated:',y)
        y2, y1 = y1, y
        if y1==y2:
            print('Double y value {}.'.format(y1))
            break
            
