#!/usr/bin/env bash

[ -e resources.go ] && rm -f resources.go
go-bindata -o=resources.go glade

# If you do need a CMD window with your app's GUI (e.g. for easier user-side debugging),
# remove the -ldflags -H=windowsgui option.
PKG_CONFIG_PATH=/usr/x86_64-w64-mingw32/sys-root/mingw/lib/pkgconfig \
CGO_ENABLED=1 CC=x86_64-w64-mingw32-gcc GOOS=windows GOARCH=amd64 \
go build

# go build -ldflags -H=windowsgui

exit 0

