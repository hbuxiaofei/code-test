#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import os.path
import time

file_path = "/tmp/log.txt"

if os.path.isfile(file_path):
    os.remove(file_path)

max_count = 20
index = 0

print("pid: {}".format(os.getpid()))


while index <= max_count:
    with open(file_path, "a+") as f:
        f.write("hello world {}\n".format(index))

    if index %2 == 0:
        if os.path.isfile(file_path):
            os.remove(file_path)

    index = index + 1
    time.sleep(1)


if os.path.isfile(file_path):
    os.remove(file_path)

