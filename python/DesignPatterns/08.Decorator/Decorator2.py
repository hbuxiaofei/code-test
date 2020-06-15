#!/usr/bin/env python3
# -*- coding: utf-8 -*-


# 修饰函数
def decorator(fun):
    def ifun(*args, **kwargs):
        args = (i+1 for i in args)
        return fun(*args, **kwargs)
    return ifun


# 被修饰函数
@decorator
def fun1(x,y,z):
    return x+y+z


# 测试代码
a = 3
b = 4
c = 5

print("%s" % fun1(a,b,c))
