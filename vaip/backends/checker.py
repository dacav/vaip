#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from vaip import (
    tree,
    errors,
)

# ------------------------------------------------------------------------

class Range(tree.Range):

    def __call__(self, v, trace):
        if self.start is not None and v < self.start:
            wrong = True
        elif self.end is not None and v > self.end:
            wrong = True
        else:
            wrong = False

        if wrong:
            if self.start and self.end:
                raise errors.InputError(
                    'Invalid x=%r: required %r <= x <= %r' % (
                        v,
                        self.start.value,
                        self.end.value,
                    ),
                    trace
                )
            elif self.start:
                raise errors.InputError(
                    'Invalid x=%r: required x >= %r' % (
                        v,
                        self.start.value,
                    ),
                    trace
                )
            elif self.end:
                raise errors.InputError(
                    'Invalid x=%r: required x <= %r' % (
                        v,
                        self.end.value,
                    ),
                    trace
                )


class Matching(tree.Matching):

    def __call__(self, v, trace):
        if self.pattern.match(v) is None:
            raise errors.InputError(
                None,
                trace,
            )

class String(tree.String):

    def __call__(self, value, trace):
        if type(value) is not str:
            raise errors.InputError(
                'Type of %r: expecting str, got %r' % (value, type(value)),
                trace,
            )
        if self.matching is not None:
            self.matching(value, trace)

class Real(tree.Real):

    def __call__(self, value, trace):
        if type(value) not in (float, int):
            raise errors.InputError(
                'Type of %r: expecting float or int, got %r' % (
                    value,
                    type(value)
                ),
                trace,
            )
        if self.range:
            self.range(value, trace)

class Int(tree.Int):

    def __call__(self, value, trace):
        if type(value) is not int:
            raise errors.InputError(
                'Type of %r: expecting int, got %r' % (
                    value,
                    type(value)
                ),
                trace,
            )
        if self.range:
            self.range(value, trace)


class Bool(tree.Bool):

    def __call__(self, value, trace):
        if type(value) is not bool:
            raise errors.InputError(
                'Type of %r: expecting bool, got %r' % (
                    value,
                    type(value)
                ),
                trace,
            )

class Array(tree.Array):

    def __call__(self, value, trace):
        if type(value) not in (list, tuple):
            raise errors.InputError(
                'Expected list or tuple',
                trace,
            )

        if self.range is not None:
            self.range(len(value), trace)
        for n, i in enumerate(value):
            trace.append(n)
            self.type(i, trace)
            trace.pop()

class Map(tree.Map):

    def __call__(self, val, trace):
        if type(val) is not dict:
            raise errors.InputError(
                'Not a mapping',
                trace,
            )

        for f in self.fields:
            f(val, trace)

class Field(tree.Field):

    def __call__(self, mapping, trace):
        val = mapping.get(self.name)
        if val is None:
            if not self.optional:
                raise errors.InputError(
                    'Missing non-optional field %r' % self.name,
                    trace
                )
        else:
            trace.append(self.name)
            self.type(val, trace)
            trace.pop()
