#!/usr/bin/env bash


[ -e resources.go ] && rm -f resources.go
go-bindata -o=resources.go ./resources/image ./resources/ui


PKG_CONFIG_PATH=/usr/x86_64-w64-mingw32/sys-root/mingw/lib/pkgconfig \
CGO_ENABLED=1 CC=x86_64-w64-mingw32-gcc GOOS=windows GOARCH=amd64 \
go build

# -ldflags -H=windowsgui

exit 0
