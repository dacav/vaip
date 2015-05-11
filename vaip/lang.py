#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# --- Battery included modules -------------------------------------------
import sys

# --- Locally installed modules -----------------------------------------
from rply import LexerGenerator, ParserGenerator

# --- Program internal modules -------------------------------------------
from vaip import tree
# ------------------------------------------------------------------------

lgen = LexerGenerator()
lgen.add('STAR', r'\*')
lgen.add('REGEX', r'/(?:(?<=\\)/|[^/])+/')
lgen.add('LPAR', r'\(')
lgen.add('RPAR', r'\)')
lgen.add('COMMA', r',')
lgen.add('COLON', r':')
lgen.add('SCOLON', r';')
lgen.add('NUMBER', '-?(?:\d+\.?\d*|\.\d+)')
lgen.add('KW_ENTRY', 'entry')
lgen.add('KW_TYPE', 'type')
lgen.add('KW_ARRAY', 'array')
lgen.add('KW_OF', 'of')
lgen.add('KW_STR', 'string')
lgen.add('KW_INT', 'int')
lgen.add('KW_REAL', 'real')
lgen.add('KW_MATCHING', 'matching')
lgen.add('KW_OPTIONAL', 'optional')
lgen.add('ID', r'[a-zA-Z_]\w*')
lgen.ignore(r'\s+')

pgen = ParserGenerator([
    'STAR', 'REGEX', 'LPAR', 'RPAR', 'COMMA', 'COLON', 'SCOLON', 'NUMBER',
    'KW_ENTRY', 'KW_TYPE', 'KW_ARRAY', 'KW_OF', 'KW_STR', 'KW_INT',
    'KW_REAL', 'KW_MATCHING', 'KW_OPTIONAL',
    'ID',
])

@pgen.production('types_list : type_def')
def type_list(p):
    yield p[0]

@pgen.production('types_list : types_list SCOLON type_def')
def type_list(p):
    yield from p[0]
    yield p[2]

@pgen.production('type_def : opt_tmod KW_TYPE ID COLON type_base')
def type_def(p):
    return tree.TypeDef(p[2].value, p[4], p[0])

@pgen.production('type_base : KW_STR opt_matching')
def type_base(p):
    return tree.String(p[1])

@pgen.production('type_base : KW_INT opt_range')
def type_base(p):
    return tree.Int(p[1])

@pgen.production('type_base : KW_REAL opt_range')
def type_base(p):
    return tree.Real(p[1])

@pgen.production('type_base : KW_ARRAY opt_range KW_OF type_base')
def type_base(p):
    return tree.Array(p[3], p[1])

@pgen.production('type_base : LPAR field_list RPAR')
def type_base(p):
    return tree.Map(p[1])

@pgen.production('type_base : ID')
def type_base(p):
    return tree.CustomType(p[0].value)

@pgen.production('field_list : field_list COMMA field')
def field_list(p):
    yield from p[0]
    yield p[2]

@pgen.production('field_list : field')
def field_list(p):
    yield p[0]

@pgen.production('field : ID COLON type_base opt_fmod')
def field(p):
    return tree.Field(p[0].value, p[2], p[3])

@pgen.production('opt_tmod : KW_ENTRY')
@pgen.production('opt_fmod : KW_OPTIONAL')
def opt_fmod(p):
    return tree.Modifier(p[0].value)

@pgen.production('opt_range : LPAR opt_number COMMA opt_number RPAR')
def opt_range(p):
    return tree.Range(p[1], p[3])

@pgen.production('opt_number : NUMBER')
def opt_number(p):
    return tree.Number(p[0].value)

@pgen.production('opt_matching : KW_MATCHING REGEX')
def opt_matching(p):
    return tree.Matching(p[1].value[1:-1])

@pgen.production('opt_tmod : ')
@pgen.production('opt_fmod : ')
@pgen.production('opt_range : ')
@pgen.production('opt_matching : ')
@pgen.production('opt_number : STAR')
def opt_any(p):
    return None
