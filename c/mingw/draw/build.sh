#!/usr/bin/env bash

NAME="Draw"

x86_64-w64-mingw32-gcc main.c -o ${NAME}.exe -lgdi32 || exit 1

exit 0
