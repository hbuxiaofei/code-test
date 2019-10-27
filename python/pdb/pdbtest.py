#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys

from func import func_test1
from func import func_test2

# pbdtest.py
def test():
    int_a = 12
    int_b = 23
    int_sum = int_a + int_b
    print("int_sum is :%d" % int_sum)


if __name__ == '__main__':
    test()
    func_test1()
    func_test2()
    sys.exit(0)
