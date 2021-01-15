#!/usr/bin/env bash

# lftp user@host
#      >mirror remotedir localdir          ：本地下载远端文件夹
#
#      >mirror -R localdir remotedir       :-R 本地上传文件夹到远端

make build

[ -d  bootimage ] && rm -rf bootimage
mkdir bootimage
cp target/x86_64-rinux/debug/bootimage-rinux.bin bootimage/
cp target/x86_64-rinux/debug/rinux bootimage/

lftp <<EOF
open ftp://wwftp:wwftp@192.168.1.252
mv /lilei/rinux/bootimage-rinux.bin /lilei/rinux/1
mv /lilei/rinux/rinux /lilei/rinux/1
close
bye
EOF

lftp <<EOF
open ftp://wwftp:wwftp@192.168.1.252
mirror -R bootimage /lilei/rinux
close
bye
EOF

[ -d  bootimage ] && rm -rf bootimage

exit 0
