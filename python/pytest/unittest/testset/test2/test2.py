#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
from common.ut import Ut
from common.cmd import Cmd

class Test2(Ut):
    @classmethod
    def setUpClass(self):
        self.number = int(0)
        self.string = "Hello world!"

    def test2_case1(self):
        self.utAssertZero(self.number, msg='result is not 0')

    def test2_case2(self):
        logging.error('raise a failure')
        self.utFail('raise a failure')

    @classmethod
    def tearDownClass(self):
        pass



