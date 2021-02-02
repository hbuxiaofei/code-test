#!/bin/sh
driver="$1"
major="$(awk -F ' ' '$2 == "'"$driver"'" { print $1 }' /proc/devices)"
mknod "/dev/edu0" c "$major" 0
