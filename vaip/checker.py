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
                entries[typedef.name] = typedef

        #print(ctx.used) TODO: warn here
        self.entries = entries

    def get_for(self, name):
        out = self.entries.get(name)
        if out is None:
            raise errors.UnboundTypeError('Not an entry type: ' + str(name))
        return out.type
