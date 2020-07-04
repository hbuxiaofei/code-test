#!/bin/bash

cd $(dirname $0)

ISO_DIR=$1

if [ ! -f "${ISO_DIR}/isolinux/isolinux.cfg" ]; then
    echo "[Err] ISO_DIR($ISO_DIR) is not exsit..."
    exit 1
fi

cp -f isolinux.cfg ${ISO_DIR}/isolinux/isolinux.cfg

echo "[Info] isolinux has been update."

exit 0

