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

    def test_array_length(self):
        counters_ck = Tests.ck.counters
        info = [0.1, 0.2, 0.3] * 3
        counters_ck(info)
        info.append(0.1)


class TestTrace(ut.TestCase):

    @classmethod
    def setUpClass(clz):
        clz.ck = checker.Checker('''
            entry type pong : array(0,10) of real(14,14.5);
            type sub_bar : (
                pong : pong
            );
            entry type deep : (
                sub : (
                    sub : (
                        foo : int(0, 1),
                        bar : sub_bar optional
                    )
                )
            );
            entry type shallow : array (0, 1) of deep
        ''')

    def verify(self, how, data, exp_trace, exp_message):
        try:
            how(data)
        except errors.InputError as e:
            trace = e.trace
            message = str(e)
        else:
            assert False, 'No exception?'
        self.assertListEqual(exp_trace, trace)
        self.assertIn(exp_message, message)

    def _verify(self, how, data, exp_trace, exp_message):
        print('>> data >> ', data)
        try:
            how(data)
        except errors.InputError as e:
            print('>>> trace >> ', e.trace, id(e.trace))
            print('>>> error >> ', e, id(e))


    def test_01(self):
        self.verify(
            TestTrace.ck.shallow,
            dict(foo=3),
            [], 'Expected list or tuple'
        )

    def test_02(self):
        tocheck = [14.0, 14.1, 14.2, 14.6, 14.4]
        self.verify(
            TestTrace.ck.pong,
            tocheck,
            [3], 'Invalid x=14.6: required  14 <= x <= 14.5'
        )

        tocheck[3] = 14     # Not a float, still ok
        TestTrace.ck.pong(tocheck)

        self.verify(
            TestTrace.ck.pong,
            tocheck * 3,        # Size beyond array boundary.
            [], 'Invalid x=15: required  0 <= x <= 10'
        )
