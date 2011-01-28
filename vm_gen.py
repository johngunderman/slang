#!/usr/bin/env python
# -*- coding: utf-8 -*-
#Author: Tim Henderson
#Email: tim.tadh@hackthology.com
#For licensing see the LICENSE file in the top level directory.


from sl_parser import Parser, Lexer
from table import SymbolTable
import il_gen, il
import vm

class generate(object):

    def __new__(cls, main, funcs):
        self = super(generate, cls).__new__(cls)
        self.__init__()
        self.var = dict()
        self.bp_offset = 0
        code = list()
        code += self.InitCode()
        code += self.Main(main, funcs)
        code += self.ExitCode()
        return code

    def InitCode(self):
        return [
            (vm.IMM, 4, 0),
            (vm.IMM, 3, 0),
            (vm.SAVE, 3, 4),
            (vm.IMM, 3, 1),
            (vm.SAVE, 3, 4),
            (vm.IMM, 3, 2),
            (vm.SAVE, 3, 4),
            (vm.IMM, 1, 3),
            (vm.IMM, 0, 0),
            (vm.IMM, 2, 0),
        ]

    def ExitCode(self):
        return [
            (vm.EXIT, 0,0)
        ]

    def Main(self, main, funcs):
        self.bp_offset = 3
        code = list()
        for i in main:
            if i.op == il.PRNT:
                code += self.Print(i)
                print code
            elif i.op == il.IMM:
                code += self.Imm(i)
                print code
            else:
                raise Exception, il.opsr[i.op]
        return code

    def Imm(self, i):
        code = [
            (vm.IMM, 3, self.bp_offset),
            (vm.ADD, 3, 0),
            (vm.IMM, 4, i.a),
            (vm.SAVE, 3, 4),
            (vm.IMM, 4, 1),
            (vm.ADD, 1, 4),
        ]
        self.var[i.result] = self.bp_offset
        self.bp_offset += 1
        return code

    def Print(self, i):
        code = [
            (vm.IMM, 3, self.var[i.a]),
            (vm.ADD, 3, 0),
            (vm.LOAD, 4, 3),
            (vm.PRNT, 4, 0)
        ]
        self.var[i.result] = self.bp_offset
        self.bp_offset += 1
        return code

if __name__ == '__main__':

    code = generate(
        *il_gen.generate(
            Parser().parse(''' print 2''', lexer=Lexer())
        )
    )
    print code
    print vm.run(code)

