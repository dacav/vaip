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
            type uid : string matching /^[0-9a-f]+$/;
            entry type user : (
                uid : uid,
                name : string optional,
                age : int(0, *) optional
            );
            entry type counters : array (*, 9) of real (0, 1)
        ''')

    def test_noentry(self):
        with self.assertRaises(errors.UnboundTypeError):
            Tests.ck['uid']

    def test_optional_nested_match(self):
        user_ck = Tests.ck.user
        with self.assertRaises(errors.InputError):
            user_ck(dict(name = 'lol')) # No uid
        with self.assertRaises(errors.InputError):
            user_ck(dict(uid = 100))
        with self.assertRaises(errors.InputError):
            user_ck(dict(uid = 'fudge'))
        user_ck(dict(uid = 'fde'))

    def test_int_range(self):
        user_ck = Tests.ck.user
        info = dict(
            uid = '91024abc',
            age = 100,
        )
        user_ck(info)
        info['age'] = -1
        with self.assertRaises(errors.InputError):
            user_ck(info)

    def test_array_real(self):
        counters_ck = Tests.ck.counters
        info = [0.1, 0.2, 0.3] * 3
        counters_ck(info)
        info.append(0.1)
        with self.assertRaises(errors.InputError):
            counters_ck(info)
        info.pop()
        info[-1] = 1.1
        with self.assertRaises(errors.InputError):
            counters_ck(info)
        info.pop()
        counters_ck(info)
        info.append('hello')
        with self.assertRaises(errors.InputError):
            counters_ck(info)
