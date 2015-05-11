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

    def _test_opt_range(self):
        check = [
            (self.parse('(1, *)'),   Range(Number(1),   None)),
            (self.parse('(1.4, *)'), Range(Number(1.4), None)),
            (self.parse('(*, 3.1)'), Range(None, Number(3.1))),
            (self.parse('(*, 2)'),   Range(None,   Number(2))),
        ]
        for got, exp in check:
            self.assertEqual(got, exp)

    def _test_opt_matching(self):
        try:
            x = self.parse('matching /cul.\./')
            x = self.parse('')
        except vaip.ParsingError as e:
            print('column', e.source_pos.colno)
            raise

    def _test_array(self):
        texts = [
            'array of int',
            'array (1, *) of real',
            'array (1, *) of real (4, 9.5)',
            'array (1, *) of string matching /foo\d/',
        ]

        for t in texts:
            x = self.parse(t)
            print(x)

    def _test_field(self):
        text = 'hello : optional array (1, *) of string matching /.ilvia/'
        x = self.parse(text)
        print(x)

    def _test_field_list(self):
        text = '(hello : optional array of string, bye : int (0, 32))'
        try:
            x = self.parse(text)
            print(x)
        except vaip.ParsingError as e:
            print(e.source_pos.colno)
            raise

    def test_typedef(self):
        texts = [
            'type uid : string matching /[0-9a-f]*/',
            '''type user : (
                uid : uid,
                name : string optional,
                age : int(-1, 5) optional
            )'''
        ]
        try:
            x = self.parse(';'.join(texts))
            print(*x, sep='\n')
        except vaip.ParsingError as e:
            print(e.source_pos.colno)
            print(e.source_pos.lineno)
            raise
