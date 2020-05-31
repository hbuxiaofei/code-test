#!/usr/bin/env bash

NAME="KeyWave"

x86_64-w64-mingw32-gcc interactive.c main.c -o ${NAME}.exe -lgdi32 || exit 1

makensis in.nsi

[ -e ${NAME}.exe ] && rm -f ${NAME}.exe

exit 0
