#!/usr/bin/env python3
# -*- coding: utf-8 -*-

class Error(Exception): pass

class SpecificationError(Error): pass
class UnboundTypeError(SpecificationError): pass
class RedefinedType(SpecificationError): pass

class NonEntry(Error): pass

class InputError(Error):

    def __init__(self, msg, trace):
        super().__init__(msg)
        self.trace = trace
