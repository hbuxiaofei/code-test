#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time

def func_test1():
    int_count = 10

    while int_count > 0:
        print("func test1")
        print("func test1 a")
        print("func test1 b")
        int_count = int_count - 1
        time.sleep(5)

def func_test2():
    print("func test2")
