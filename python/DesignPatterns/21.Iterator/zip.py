#!/usr/bin/env python3
# -*- coding: utf-8 -*-

a = [1,2,3]
b = [4,5,6]
zipped = zip(a,b)     # 打包为元组的列表

for z in zipped:
    print(z)
