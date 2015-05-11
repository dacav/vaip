#!/usr/bin/env python
# -*- coding: utf-8 -*-

# --- Battery included modules -------------------------------------------
import unittest as ut

# --- Locally installed modules -----------------------------------------
# --- Program internal modules -------------------------------------------
from vaip import (
    checker,
    errors,
)

# ------------------------------------------------------------------------

class Tests(ut.TestCase):

    @classmethod
    def setUpClass(clz):
        clz.ck = checker.Checker('''
            type uid : string matching /[0-9a-f]*/;
            entry type user : (
                uid : uid,
                name : string optional,
                age : int(0, *) optional
            );
            entry type counters : array (*, 10) of real (0, 1)
        ''')

    def test_noentry(self):
        with self.assertRaises(errors.UnboundTypeError):
            Tests.ck.get_for('uid')

    def test_entry_1(self):
        user_ck = Tests.ck.get_for('user')
        user_ck( dict(uid = 100) )
