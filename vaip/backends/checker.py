#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from vaip import (
    tree,
    errors,
)

# ------------------------------------------------------------------------

class Range(tree.Range):

    def __call__(self, v):
        if self.start is not None and v < self.start:
            raise errors.InputError()
        if self.end is not None and v > self.end:
            raise errors.InputError()

class Matching(tree.Matching):

    def __call__(self, v):
        if self.pattern.match(v) is None:
            raise errors.InputError()

class String(tree.String):

    def __call__(self, val):
        if type(val) is not str:
            raise errors.InputError()
        if self.matching is not None:
            self.matching(val)

class Real(tree.Real):

    def __call__(self, value):
        if type(value) is not float:
            raise errors.InputError()
        if self.range:
            self.range(value)

class Int(tree.Int):

    def __call__(self, value):
        if type(value) is not int:
            raise errors.InputError()
        if self.range:
            self.range(value)

class Array(tree.Array):

    def __call__(self, value):
        if self.range is not None:
            try:
                self.range(len(value))
            except TypeError:
                raise errors.InputError()   # No len
        try:
            items = iter(value)
            if items is value:
                raise errors.InputError()   # would consume
        except TypeError:
            raise errors.InputError()   # Not iterable
        for i in items:
            self.type(i)

class Map(tree.Map):

    def __call__(self, val):
        if type(val) is not dict:
            raise errors.InputError()

        for f in self.fields:
            f(val)

class Field(tree.Field):

    def __call__(self, mapping):
        val = mapping.get(self.name)
        if val is None:
            if not self.optional:
                raise errors.InputError()
        else:
            self.type(val)
