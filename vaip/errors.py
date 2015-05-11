#!/usr/bin/env python3
# -*- coding: utf-8 -*-

class Error(Exception): pass

class SpecificationError(Error): pass
class UnboundTypeError(SpecificationError): pass
class RedefinedType(SpecificationError): pass

class InputError(Error): pass
