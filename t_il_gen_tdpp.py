#!/usr/bin/env python
# -*- coding: utf-8 -*-
#Author: Tim Henderson
#Email: tim.tadh@hackthology.com
#For licensing see the LICENSE file in the top level directory.

import cStringIO

from sl_parser_tdpp import Parser, Lex
from table import SymbolTable
import il_gen, il
import nose

parser = Parser(Lex, debug=False)
def run(s):
    out = cStringIO.StringIO()
    il.run(*il_gen.generate(parser.parse(s)), stdout=out)
    return out.getvalue()

def t_expr_const():
    assert '2' == run('print 2').rstrip('\n')

def t_expr_ops():
    assert '6' == run('print 2*3').rstrip('\n')
    assert '6' == run('print 1+2+3').rstrip('\n')
    assert '6' == run('print 9-3').rstrip('\n')
    assert '6' == run('print 12/2').rstrip('\n')

def t_expr_compound():
    assert str(4*3/2) == run('print 4*3/2').rstrip('\n')
    assert str(4/2*3) == run('print 4/2*3').rstrip('\n')
    assert str((3+9)*4/8) == run('print (3+9)*4/8').rstrip('\n')
    assert str(((9-3)+(5-3))/2 + 2) == run('print ((9-3)+(5-3))/2 + 2').rstrip('\n')
    assert str(5 * 4 / 2 - 10 + 5 - 2 + 3) == run('print 5 * 4 / 2 - 10 + 5 - 2 + 3').rstrip('\n')
    assert str(5 / 4 * 2 + 10 - 5 * 2 / 3) == run('print 5 / 4 * 2 + 10 - 5 * 2 / 3').rstrip('\n')

def t_func_call():
    assert str(5 / 4 * 2 + 10 - 5 * 2 / 3) == run('''
        f = func() { return 5 / 4 * 2 + 10 - 5 * 2 / 3 }
        print f()
        ''').rstrip('\n')

def t_func_uppernames():
    assert str(5 / 4 * 2 + 10 - 5 * 2 / 3) == run('''
        g = func() {
            g1 = func() { return g2() }
            g2 = func() { return g3() }
            g3 = func() { return h() }
            return g1()
        }
        h = func() { return f() }
        f = func() { return 5 / 4 * 2 + 10 - 5 * 2 / 3 }
        print g()
        ''').rstrip('\n')

def t_func_pointers():
    assert str(5 / 4 * 2 + 10 - 5 * 2 / 3) == run('''
        f = func() { return 5 / 4 * 2 + 10 - 5 * 2 / 3 }
        g = func(h) { return h() }
        print g(f)
        ''').rstrip('\n')

def t_func_params_simple():
    assert str(4) == run('''
        sub = func(a, b) { return a - b }
        print sub(5+7, 8)
        ''').rstrip('\n')

def t_func_params_stack():
    assert str(4) == run('''
        sub = func(a, b) {
            _sub = func() {
                return a - b
            }
            return _sub()
        }
        print sub(5+7, 8)
        ''').rstrip('\n')

def t_if():
    raise nose.SkipTest
    assert str(2) == run('''
        if (1 > 2) {
            print 1
        } else {
            print 2
        }
        ''').rstrip('\n')
    assert str(1) == run('''
        if (1 < 2) {
            print 1
        } else {
            print 2
        }
        ''').rstrip('\n')


def t_if_set():
    raise nose.SkipTest
    assert str(2) == run('''
        if (1 > 2) {
            a = 1
        } else {
            a = 2
        }
        print a
        ''').rstrip('\n')
    assert str(1) == run('''
        if (1 < 2) {
            a = 1
        } else {
            a = 2
        }
        print a
        ''').rstrip('\n')