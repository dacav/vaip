#!/usr/bin/env python
# -*- coding: utf-8 -*-

# --- Battery included modules -------------------------------------------
import sys
import unittest as ut

# --- Locally installed modules -----------------------------------------
# --- Program internal modules -------------------------------------------
import vaip
from vaip.tree import *

# ------------------------------------------------------------------------

class Tests(ut.TestCase):

    def setUp(self):
        parse = vaip.pgen.build().parse
        lex = vaip.lgen.build().lex

        def p(text):
            toks = list(lex(text))
            return parse(iter(toks))

        self.parse = p

    def test_opt_range(self):
        check = [
            ('(1, *)',   Range(Number(1),   None)),
            ('(1.4, *)', Range(Number(1.4), None)),
            ('(*, 3.1)', Range(None, Number(3.1))),
            ('(*, 2)',   Range(None,   Number(2))),
        ]
        for text, exp in check:
            only, *slurp = self.parse('type x : int ' + text)
            self.assertEqual(len(slurp), 0)
            self.assertEqual(only.type.range, exp)

    def test_typedef(self):
        text = '''
            type uid : string matching /[0-9a-f]*/;
            entry type user : (
                uid : uid,
                name : string optional,
                age : int(0, *) optional
            );
            type counters : array (*, 10) of real (0, 1)
        '''
        l1, l2, l3 = self.parse(text)

        self.assertEqual(l1.name, 'uid')
        self.assertIsNotNone(l1.type.matching.match('0125af'))
        self.assertIsNone(l1.mod)

        self.assertEqual(l2.name, 'user')
        self.assertEqual(l2.mod.name, 'entry')

        l21, l22, l23 = l2.type.fields
        self.assertEqual(l21.name, 'uid')
        self.assertEqual(l21.mod, None)
        self.assertEqual(l21.type.name, 'uid')

        self.assertEqual(l3.name, 'counters')
        self.assertEqual(l3.mod, None)
        self.assertEqual(l3.type.type.range, Range(Number(0), Number(1)))
        self.assertEqual(l3.type.range, Range(None, Number(10)))
