#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
from common.ut import Ut
from common.cmd import Cmd

class Test1(Ut):

    @classmethod
    def setUpClass(self):
        self.result=int(0)
        print('set up start ...')

    def test1_case1_1(self):
        cmd = 'virsh iface-list --all'
        command = Cmd()
        stdout, stderr = command.run(cmd)
        if stdout.strip():
            logging.info('%s\n%s' % (cmd, stdout))
        else:
            logging.error('%s\n%s' % (cmd, stderr))
        if stderr:
            self.utFail('%s failed(%s)' % (cmd, stderr))

    def test1_case1_2(self):
        cmd = 'virsh domblklist'
        command = Cmd()
        stdout, stderr = command.run(cmd)
        if stdout.strip():
            logging.info('%s\n%s' % (cmd, stdout))
        else:
            logging.error('%s\n%s' % (cmd, stderr))
        if stderr:
            self.utFail('%s failed(%s)' % (cmd, stderr))

    def test1_case2(self):
        errno = 0
        self.utAssertZero(errno,
                          msg='errno(%d) is not %d' % (errno, self.result))

    def test1_case3(self):
        errno = 3
        self.utAssertZero(errno,
                          msg='errno(%d) is not %d' % (errno, self.result))

    def test1_case4(self):
        errno = 4
        self.utSkip('Skip test for errno is 4')

        self.utAssertExpr(self.result == errno,
                          msg='errno(%d) is not %d' % (errno, self.result))

    def test1_case5(self):
        string = 'Hello world!'
        self.utAssertString(string, msg='string is null')

    def test1_case6(self):
        string = ' '
        self.utAssertString(string, msg='string is null')

    @classmethod
    def tearDownClass(self):
        pass

