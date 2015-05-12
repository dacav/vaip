#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# --- Battery included modules -------------------------------------------
import unittest as ut
import re
from operator import attrgetter as aget

# --- Locally installed modules -----------------------------------------
# --- Program internal modules -------------------------------------------
from vaip import lang

# ------------------------------------------------------------------------

class Test(ut.TestCase):

    get = aget('name', 'value')

    def setUp(self):
        self.lex = lang.lgen.build().lex

    def test_re(self):
        tks = map(Test.get, self.lex('* /cu.*stom/ /^re/ /gex$/ /test\/a/'))
        self.assertTupleEqual(next(tks), ('STAR', '*'))
        self.assertTupleEqual(next(tks), ('REGEX', '/cu.*stom/'))
        self.assertTupleEqual(next(tks), ('REGEX', '/^re/'))
        self.assertTupleEqual(next(tks), ('REGEX', '/gex$/'))
        self.assertTupleEqual(next(tks), ('REGEX', '/test\\/a/'))

