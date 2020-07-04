#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest

class Ut(unittest.TestCase):

    def utFail(self, msg=None):
        self.fail(msg)

    def utAssertZero(self, num=0, msg=None):
        self.assertEqual(0, num, msg)

    def utAssertString(self, string=None, msg=None):
        if string is None or not string.strip():
            self.fail(msg)

    def utAssertExpr(self, expr, msg=None):
        self.assertTrue(expr, msg)

    def utSkip(self, msg=None):
        unittest.skip(msg)

