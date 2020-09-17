#!/usr/bin/env bash

# lftp user@host
#      >mirror remotedir localdir          ：本地下载远端文件夹
#
#      >mirror -R localdir remotedir       :-R 本地上传文件夹到远端

FTP_IP="<>"
FTP_USER="<>"
FTP_PASSWD="<>"


[ -d  bootimage ] && rm -rf bootimage
mkdir bootimage
cp target/x86_64-rinux/debug/bootimage-rinux.bin bootimage/

lftp <<EOF
open ftp://${FTP_USER}:${FTP_PASSWD}@${FTP_IP}
mv /lilei/rinux/bootimage-rinux.bin /lilei/rinux/1
close
bye
EOF


lftp <<EOF
open ftp://${FTP_USER}:${FTP_PASSWD}@${FTP_IP}
mirror -R bootimage /lilei/rinux
close
bye
EOF
