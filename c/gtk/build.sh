#!/usr/bin/env bash


PKG_CONFIG_TOOL="x86_64-w64-mingw32-pkg-config"
PKG_CONFIG_CC="x86_64-w64-mingw32-gcc"

${PKG_CONFIG_CC} -Wall -mwindows main.c -o hello.exe \
`${PKG_CONFIG_TOOL} gtk+-3.0 --cflags` \
`${PKG_CONFIG_TOOL} gtk+-3.0 --libs`



