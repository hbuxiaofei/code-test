#!/usr/bin/env bash

# If you do need a CMD window with your app's GUI (e.g. for easier user-side debugging),
# remove the -ldflags -H=windowsgui option.
PKG_CONFIG_PATH=/usr/x86_64-w64-mingw32/sys-root/mingw/lib/pkgconfig \
CGO_ENABLED=1 CC=x86_64-w64-mingw32-gcc GOOS=windows GOARCH=amd64 \
go build -ldflags -H=windowsgui

exit 0

CGO_ENABLED=1 CC=x86_64-w64-mingw32-gcc GOOS=windows GOARCH=amd64 \
go build -ldflags '-s -w --extldflags "-static -fpic"' ./main.go
exit 0

PKG_CONFIG_PATH=/usr/x86_64-w64-mingw32/sys-root/mingw/lib/pkgconfig \
CGO_ENABLED=1 CC=x86_64-w64-mingw32-gcc GOOS=windows GOARCH=amd64 \
go build -ldflags -H=windowsgui
exit 0

# PKG_CONFIG_PATH=/usr/x86_64-w64-mingw32/lib/pkgconfig
PKG_CONFIG_PATH=/usr/x86_64-w64-mingw32/sys-root/mingw/lib/pkgconfig \
CGO_ENABLED=1 \
CC=x86_64-w64-mingw32-gcc \
GOOS=windows \
GOARCH=amd64 \
go install github.com/gotk3/gotk3/gtk

exit 0




