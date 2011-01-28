#!/usr/bin/env python
# -*- coding: utf-8 -*-
#Author: Tim Henderson
#Email: tim.tadh@hackthology.com
#For licensing see the LICENSE file in the top level directory.


from sl_parser import Parser, Lexer
from table import SymbolTable
import il

prebuilt_funcs = {
    'print':il.Func([{'type':il.Int(), 'name':None}], []),
    '__add':il.Func(
        [{'type':il.Int(), 'name':None}, {'type':il.Int(), 'name':None}],
        [{'type':il.Int(), 'name':None}]
    ),
    'exit':il.Func([], [])
}

class generate(object):

    def __new__(cls, root):
        self = super(generate, cls).__new__(cls)
        self.__init__()
        r = self.Exprs(root)
        r += [ il.Inst(il.PRNT, r[-1].result, 0, 0)]
        print r
        return r

    def __init__(self):
        self.functions = dict()
        self.fcount = 0
        self.tcount = 0
        self.objs = SymbolTable(prebuilt_funcs)

    def tmp(self):
        self.tcount += 1
        return 't%i' % self.tcount

    def Exprs(self, node):
        assert node.label == 'Exprs'
        code = list()
        for c in node.children:
            if c.label == 'Assign':
                code += self.Assign(c)
            elif c.label == 'Arith':
                code += self.Arith(c)
            else:
                raise Exception, c.label
        return code

    def Assign(self, node):
        assert node.label == 'Assign'
        name = node.children[0]
        c = node.children[1]
        if c.label == 'Arith':
            code = self.Arith(c)
        else:
            raise Exception
        self.objs[name] = code[-1].result
        return code

    def Arith(self, node):
        if node.label == 'Arith':
            c = node.children[0]
        else:
            c = node
        if c.label == 'INT':
            return self.Int(c.children[0])
        elif c.label == '/' or c.label == '*' or c.label == '-' or c.label == '+':
            return self.Op(c)
        elif c.label == 'NAME':
            return [ il.Inst('USE', 0, 0, self.objs[c.children[0]]) ]
        else:
            raise Exception, 'Unexpected Node %s' % str(c)

    def Op(self, node):
        ops = {'/':'DIV', '*':'MUL', '-':'SUB', '+':'ADD'}
        A = self.Arith(node.children[0])
        B = self.Arith(node.children[1])
        ar = A[-1].result
        br = B[-1].result
        if A[-1].op == 'USE': A = A[:-1]
        if B[-1].op == 'USE': B = B[:-1]
        return A + B + [
            il.Inst(il.ops[ops[node.label]],
            ar,
            br,
            self.tmp())
        ]

    def Int(self, node):
        return [ il.Inst(il.IMM, node, 0, self.tmp()) ]


    # ------------------------------------------------------------------------ #


if __name__ == '__main__':

    print il.run(generate(Parser().parse(''' 2*3/(4-5*(12*32-15)) ''', lexer=Lexer())))
    print il.run(generate(Parser().parse(''' 2 ''', lexer=Lexer())))
    print il.run(generate(Parser().parse(''' x = 2*3/(4-5*(12*32-15))
        y = x+2 ''', lexer=Lexer())))
