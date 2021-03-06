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
                age : int(0, *) optional,
                geek : bool optional
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

    def test_bool(self):
        user_ck = Tests.ck.user
        info = dict(
            uid = '91024abc',
            geek = True
        )
        user_ck(info)
        info['geek'] = 1
        with self.assertRaises(errors.InputError):
            user_ck(info)
        info['geek'] = False
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

    def test_shallow(self):
        self.verify(
            TestTrace.ck.shallow,
            dict(foo=3),
            [], 'Expected list or tuple'
        )

    def test_pong(self):
        tocheck = [14.0, 14.1, 14.2, 14.6, 14.4]
        self.verify(
            TestTrace.ck.pong,
            tocheck,
            [3], 'Invalid x=14.6: required 14 <= x <= 14.5'
        )

        tocheck[3] = 14     # Not a float, still ok
        TestTrace.ck.pong(tocheck)

        self.verify(
            TestTrace.ck.pong,
            tocheck * 3,        # Size beyond array boundary.
            [], 'Invalid x=15: required 0 <= x <= 10'
        )

    def test_deep(self):
        tocheck = dict()
        self.verify(TestTrace.ck.deep, tocheck,
            [], 'Missing non-optional field \'sub\''
        )
        tocheck['sub'] = dict()
        self.verify(TestTrace.ck.deep, tocheck,
            ['sub'], 'Missing non-optional field \'sub\''
        )
        tocheck['sub']['sub'] = dict()
        self.verify(TestTrace.ck.deep, tocheck,
            ['sub', 'sub'], 'Missing non-optional field \'foo\''
        )
        tocheck['sub']['sub']['foo'] = 'hello'
        self.verify(TestTrace.ck.deep, tocheck,
            ['sub', 'sub', 'foo'], "Type of 'hello': expecting int, got <class 'str'>"
        )
        tocheck['sub']['sub']['foo'] = 99
        self.verify(TestTrace.ck.deep, tocheck,
            ['sub', 'sub', 'foo'], 'Invalid x=99: required 0 <= x <= 1'
        )
        tocheck['sub']['sub']['foo'] = 1
        TestTrace.ck.deep(tocheck)

        tocheck['sub']['sub']['bar'] = '12'
        self.verify(TestTrace.ck.deep, tocheck,
            ['sub', 'sub', 'bar'], 'Not a mapping'
        )

        tocheck['sub']['sub']['bar'] = dict(
            pong=[14.0, 14.1, 14.2, 14.9]
        )
        self.verify(TestTrace.ck.deep, tocheck,
            ['sub', 'sub', 'bar', 'pong', 3],
            'Invalid x=14.9: required 14 <= x <= 14.5'
        )
