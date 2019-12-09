#!/usr/bin/env bash

# https://github.com/rhinstaller/anaconda/pyanaconda/display.py
# DISPLAY=:1 ./app
#
# Other example:
#   /usr/bin/Xorg :1 vt1 -keeptty
#   systemctl restart console-gettty
#
X_DISPLAY_NUMBER=1
/usr/bin/Xorg -br -logfile /tmp/X.log :$X_DISPLAY_NUMBER vt1 -s 1440 \
    -ac -nolisten tcp -dpi 96 -noreset
