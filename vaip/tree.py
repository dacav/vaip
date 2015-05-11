#!/usr/bin/env python
# -*- coding: utf-8 -*-

# --- Battery included modules -------------------------------------------
import sys
import re
import functools as ft

# --- Locally installed modules -----------------------------------------
# --- Program internal modules -------------------------------------------
from rply.token import BaseBox

# ------------------------------------------------------------------------

@ft.total_ordering
class Number(BaseBox):

    def __init__(self, v):
        super().__init__()
        if type(v) not in (int, float):
            try:
                v = int(v)
            except:
                v = float(v)
        self.value = v

    def __lt__(self, oth):
        return False if oth is None else self.value < oth.value

    def __eq__(self, oth):
        if oth is None:
            return False
        return self.value == oth.value

    def __repr__(self):
        return 'Number(%r)' % self.value


class Range(BaseBox):

    def __init__(self, start, end):
        super().__init__()
        assert None in (start, end) or start <= end
        self.start = start
        self.end = end

    def __lt__(self, oth):
        if oth is None:
            return False
        return self.start < oth.start or self.end < oth.end

    def __eq__(self, oth):
        if oth is None:
            return False
        return self.start == oth.start and self.end == oth.end

    def __repr__(self):
        return 'Range(start=%r, end=%r)' % (self.start, self.end)


class Matching(BaseBox):

    def __init__(self, pattern):
        super().__init__()
        self.pattern = re.compile(pattern)

    @property
    def match(self):
        return self.pattern.match

    def __repr__(self):
        return 'Match(%r)' % self.pattern

class String(BaseBox):

    def __init__(self, matching=None):
        super().__init__()
        self.matching = matching

    def __repr__(self):
        if self.matching is None:
            return 'String()'
        return 'String(matching=%r)' % self.matching

class Real(BaseBox):

    def __init__(self, range=None):
        super().__init__()
        self.range = range

    def __repr__(self):
        return 'Real(range=%r)' % self.range

class Int(BaseBox):

    def __init__(self, range=None):
        super().__init__()
        self.range = range

    def __repr__(self):
        return 'Int(range=%r)' % self.range

class Array(BaseBox):

    def __init__(self, type, range=None):
        super().__init__()
        self.type = type
        self.range = range

    def __repr__(self):
        return 'Array(type=%r, range=%r)' % (self.type, self.range)


class Map(BaseBox):

    def __init__(self, fields):
        super().__init__()
        if iter(fields) is fields:
            fields = list(fields)
        self.fields = fields

    def __repr__(self):
        return 'Map(fields=%r)' % self.fields


class Field(BaseBox):

    def __init__(self, name, type, mod):
        super().__init__()
        self.name = name
        self.type = type
        self.mod = mod

    def __repr__(self):
        return 'Field(name=%r, type=%r, mod=%r)' % (
            self.name, self.type, self.mod
        )

    @property
    def optional(self):
        return self.mod is not None and self.mod.name == 'optional'

class Modifier(BaseBox):

    def __init__(self, name):
        super().__init__()
        self.name = name

    def __repr__(self):
        return 'Modifier(name=%r)' % self.name

class TypeDef(BaseBox):

    def __init__(self, name, type, mod):
        super().__init__()
        self.name = name
        self.type = type
        self.mod = mod

    def __repr__(self):
        return 'TypeDef(name=%r, type=%r, mod=%r)' % (
            self.name, self.type, self.mod
        )

    def __eq__(self, other):
        if other is None:
            return False
        return self.name == other.name

    def __lt__(self):
        if other is None:
            return False
        return self.name < other.name

    @property
    def entry(self):
        return self.mod is not None and self.mod.name == 'entry'
