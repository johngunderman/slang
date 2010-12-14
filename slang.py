#!/usr/bin/env python
# -*- coding: utf-8 -*-
#Author: Tim Henderson
#Email: tim.tadh@hackthology.com
#For licensing see the LICENSE file in the top level directory.

import functools

LOAD = 0x0
SAVE = 0x1
IMM  = 0x2
J    = 0x3
PC   = 0x4
ADD  = 0x5
SUB  = 0x6
MUL  = 0x7
DIV  = 0x8
EXIT = 0x9
PRIN = 0xa

A = [J, PC]
B = [LOAD, IMM, ADD, SUB, MUL, DIV]
C = [SAVE]

def load(regs, stack, pc, r1, r2):
    regs[r1] = stack[regs[r2]]
    return pc + 1
def save(regs, stack, pc, r1, r2):
    print r1, r2, ':',  regs[r1], regs[r2]
    print len(stack), len(stack) == regs[r2]
    if len(stack) == regs[r2]:
        stack.append(regs[r1])
        print stack
    elif len(stack) < regs[r2]:
        raise Exception, "Address out of range"
    else:
        stack[regs[r2]] = regs[r1]
    return pc + 1
def imm(regs, stack, pc, reg, immediate):
    regs[reg] = immediate
    return pc + 1
def j(regs, stack, pc, reg, addr):
    return addr
def pc(regs, stack, pc, reg, addr):
    regs[reg] = pc + 1
    return pc + 1
def add(regs, stack, pc, r1, r2):
    print '->', regs[r1], regs[r2], regs[r1] + regs[r2]
    regs[r1] += regs[r2]
    return pc + 1
def sub(regs, stack, pc, r1, r2):
    regs[r1] -= regs[r2]
    return pc + 1
def mul(regs, stack, pc, r1, r2):
    regs[r1] *= regs[r2]
    return pc + 1
def div(regs, stack, pc, r1, r2):
    regs[r1] /= regs[r2]
    return pc + 1
def prin(regs, stack, pc, r1, r2):
    print '>>>>>', regs[r1]
    return pc + 1

INSTS = {
    LOAD:load, SAVE:save, IMM:imm, J:j, PC:pc, ADD:add, SUB:sub, MUL:mul,
    DIV:div, PRIN:prin
}

def run(program):
    regs = [0, 0, 0, 0, 0]
    stack = list()
    pc = 0
    inst = program[pc]
    while True:
        print 'pc =', pc
        print 'inst =', inst
        print 'regs =', regs
        print 'stack =', stack
        op = inst[0]
        if op == EXIT: break
        if op in A:
            reg = inst[1]
            addr = None
        elif op in B:
            reg = inst[1]
            addr = inst[2]
        else:
            reg = inst[2]
            addr = inst[1]
        pc = INSTS[op](regs, stack, pc, reg, addr)
        inst = program[pc]
        print


if __name__ == '__main__':
    run([
#init prog
        (IMM, 4, 0),
        (IMM, 3, 0),
        (SAVE, 3, 4),
        (IMM, 3, 1),
        (SAVE, 3, 4),
        (IMM, 3, 2),
        (SAVE, 3, 4),
        (IMM, 1, 3),
# start prog
        (IMM, 4, 0),
        (ADD, 4, 1),
        (IMM, 3, 29),
        (SAVE, 4, 3, 'save arg 1'),
        (IMM, 3, 1),
        (ADD, 4, 3),
        (IMM, 3, 37),
        (SAVE, 4, 3, 'save arg 2'),
        (ADD, 4, 4),

#func add
    #stack save
        (IMM, 4, 0),
        (ADD, 4, 1),
        (IMM, 3, 2),
        (ADD, 4, 3, 'reg[4] += 2'),
        (SAVE, 4, 0, 'stack save: save bp'),
        (IMM, 3, 1),
        (ADD, 4, 3, 'reg[4] += 1'),
        (SAVE, 4, 1, 'stack save: save fp'),
        (ADD, 4, 3, 'reg[4] += 1'),
        (SAVE, 4, 2, 'stack save: save ra'),
        (ADD, 4, 3, 'reg[4] += 1'),
        (IMM, 0, 0),
        (ADD, 0, 1, 'mv fp to bp'),
        (IMM, 1, 0),
        (ADD, 1, 4, 'mv $4 to fp'),
    # start func body
        (IMM, 3, 0), # load args
        (ADD, 3, 0),
        (IMM, 4, 1),
        (ADD, 4, 0),
        (LOAD, 3, 3),
        (LOAD, 4, 4),
        (ADD, 4, 3), # do addition

        (SAVE, 1, 4), # save result
        (IMM, 3, 1),
        (ADD, 1, 3, 'reg[1] += 1'),

        (IMM, 3, 15),
        (ADD, 4, 3),

        (SAVE, 1, 4), # save result
        (IMM, 3, 1),
        (ADD, 1, 3, 'reg[1] += 1'),
    # end func body
    #stack restore
        (IMM, 4, 0),
        (ADD, 4, 0, 'load bp into 4'),
        (IMM, 3, 2),
        (ADD, 4, 3, 'reg[4] += 2'),
        (LOAD, 0, 4, 'stack restore: bp'),
        (IMM, 3, 2),
        (ADD, 4, 3, 'reg[4] += 2'),
        (LOAD, 2, 4, 'stack restore: ra'),
        (IMM, 3, 1),
        (SUB, 4, 3, 'reg[4] += 1'),
        (IMM, 3, 0),
        (ADD, 3, 1),
        (LOAD, 1, 4, 'stack restore: fp'),
        (IMM, 4, 2),
        (SUB, 3, 4),
        (LOAD, 4, 3, 'function return loaded'),
        (SAVE, 1, 4, 'save result'), # save result
        (IMM, 4, 1),
        (ADD, 1, 4, 'inc fp'),

        (IMM, 4, 1),
        (ADD, 3, 4),
        (LOAD, 4, 3, 'function return loaded'),
        (SAVE, 1, 4, 'save result'), # save result
        (IMM, 4, 1),
        (ADD, 1, 4, 'inc fp'),
#end func
        (IMM, 3, 0),
        (ADD, 3, 1),
        (IMM, 4, 2),
        (SUB, 3, 4),
        (LOAD, 3, 3),
        (PRIN, 3, 3),

        (IMM, 3, 0),
        (ADD, 3, 1),
        (IMM, 4, 1),
        (SUB, 3, 4),
        (LOAD, 3, 3),
        (PRIN, 3, 3),
    #exit
        (EXIT, 0, 0),
    ])
