#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from vaip.lang import pgen, lgen, ParseContext
from vaip import errors

class Checker:

    def __init__(self, specification):
        parse = pgen.build().parse
        lex = lgen.build().lex
        entries = dict()
        ctx = ParseContext()
        for typedef in parse(lex(specification), ctx):
            if typedef.entry:
                cb = entries[typedef.name] = typedef.type
                try:
                    # Might fail if this type has a reserved name in
                    # python. Still accessible with [] notation
                    setattr(self, typedef.name, cb)
                except:
                    # TODO: warning here
                    pass

        #print(ctx.used) TODO: warning here
        self.__entries = entries

    def __getitem__(self, name):
        out = self.__entries.get(name)
        if out is None:
            raise errors.UnboundTypeError('Not an entry type: ' + str(name))
        return out
