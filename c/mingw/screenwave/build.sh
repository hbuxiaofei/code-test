#!/usr/bin/env bash

NAME="ScreenWare"

x86_64-w64-minigw32-gcc ./main.c -o ${NAME}.exe || exit 1

makensis ./in.nsi

[ -e ${NAME}.exe ] && rm -f ${NAME}.exe

exit 0
