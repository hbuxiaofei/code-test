#!/usr/bin/env python
# -*- coding: utf-8 -*-

import subprocess

class Cmd():
    def run(self, cmd):
        p = subprocess.Popen(cmd, shell=True, stdout = subprocess.PIPE, stderr = subprocess.PIPE)
        stdout, stderr = p.communicate()
        return stdout, stderr


if __name__=='__main__':
    command = Cmd()
    cmd = 'ls -al'
    stdout, stderr = command.run(cmd)
    print('>>> %s: \n%s\n' % (cmd, stdout))
    if stderr:
        print('>>> [Err]%s: \n%s\n' % (cmd, stderr))

