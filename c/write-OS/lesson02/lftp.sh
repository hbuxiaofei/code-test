#!/usr/bin/env bash

#!/usr/bin/env bash

# lftp user@host
#      >mirror remotedir localdir          ：本地下载远端文件夹
#
#      >mirror -R localdir remotedir       :-R 本地上传文件夹到远端


[ -d  bootimage ] && rm -rf bootimage
mkdir bootimage

cp -f bootsect.s bootimage/
cp -f floppy.s bootimage/
cp -f Makefile bootimage/

lftp <<EOF
open ftp://wwftp:wwftp@192.168.1.252
mv /lilei/rinux/floppy.s /lilei/rinux/1
mv /lilei/rinux/bootsect.s /lilei/rinux/1
mv /lilei/rinux/Makefile /lilei/rinux/1
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
make clean

exit 0

