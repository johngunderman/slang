#!/usr/bin/env python
# -*- coding: utf-8 -*-
#Author: Tim Henderson
#Email: tim.tadh@hackthology.com
#For licensing see the LICENSE file in the top level directory.

import sys

typesr = (
    'CHAIN', 'IF_THEN', 'IF_THEN_ELSE',
)
types = dict((k, i) for i, k in enumerate(typesr))
sys.modules[__name__].__dict__.update(types)

class Node(object):

    def __init__(self, rtype, blks):
        self.region_type = rtype
        self.blks = blks

    def __repr__(self): return str(self)

    def __str__(self):
        return (
            '<cf.Node region:%s>'
        ) % (self.region_type,)