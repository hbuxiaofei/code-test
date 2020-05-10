#!/usr/bin/env bash

NAME="ScreenWave"

x86_64-w64-mingw32-gcc main.c -o ${NAME}.exe -lgdi32 || exit 1
exit 0
makensis in.nsi

[ -e ${NAME}.exe ] && rm -f ${NAME}.exe

exit 0
