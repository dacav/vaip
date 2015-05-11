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
        try:
            v = int(v)
        except:
            v = float(v)
        self.__v = v

    def __lt__(self, oth):
        return False if oth is None else self.__v < oth.__v

    def __eq__(self, oth):
        return False if oth is None else self.__v == oth.__v

    def __repr__(self):
        return 'Number(%r)' % self.__v

class Range(BaseBox):

    def __init__(self, start, end):
        super().__init__()
        assert None in (start, end) or start <= end
        self.__start = start
        self.__end = end

    def __lt__(self, oth):
        return self.__start < oth.__start or self.__end < oth.__end

    def __eq__(self, oth):
        return self.__start == oth.__start and self.__end == oth.__end

    def __repr__(self):
        return 'Range(%r, %r)' % (self.__start, self.__end)

class Matching(BaseBox):

    def __init__(self, pattern):
        super().__init__()
        self.__pattern = re.compile(pattern)

    def __repr__(self):
        return 'Match(%r)' % self.__pattern

class String(BaseBox):

    def __init__(self, matching=None):
        super().__init__()
        self.__matching = matching

    def __repr__(self):
        if self.__matching is None:
            return 'String'
        return 'String(%r)' % self.__matching

class Real(BaseBox):

    def __init__(self, range=None):
        super().__init__()
        self.__range = range

    def __repr__(self):
        return 'Real(range=%r)' % self.__range

class Int(BaseBox):

    def __init__(self, range=None):
        super().__init__()
        self.__range = range

    def __repr__(self):
        return 'Int(range=%r)' % self.__range

class Array(BaseBox):

    def __init__(self, type, range=None):
        super().__init__()
        self.__type = type
        self.__range = range

    def __repr__(self):
        return 'Array(type=%r, range=%r)' % (self.__type, self.__range)


class Map(BaseBox):

    def __init__(self, fields):
        super().__init__()
        if iter(fields) is fields:
            fields = list(fields)
        self.__fields = fields

    def __repr__(self):
        return 'Map(fields=%r)' % self.__fields


class Field(BaseBox):

    def __init__(self, name, type, mod):
        super().__init__()
        self.__name = name
        self.__type = type
        self.__mod = mod

    def __repr__(self):
        return 'Field(name=%r, type=%r, mod=%r)' % (
            self.__name, self.__type, self.__mod
        )

class Modifier(BaseBox):

    def __init__(self, name):
        super().__init__()
        self.__name = name

    def __repr__(self):
        return 'Modifier(%r)' % self.__name

class TypeDef(BaseBox):

    def __init__(self, name, type):
        super().__init__()
        self.__name = name
        self.__type = type

    def __repr__(self):
        return 'TypeDef(name=%r, type=%r)' % (
            self.__name, self.__type
        )

class CustomType(BaseBox):

    def __init__(self, name):
        super().__init__()
        self.__name = name

    def __repr__(self):
        return 'CustomType(%r)' % self.__name
