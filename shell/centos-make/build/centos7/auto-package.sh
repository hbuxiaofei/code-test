#!/bin/bash

set -e 

EXEC_NAME="auto-package.sh"
IN_ARGS=`getopt -o hi:o: --long help,iso:,out: -n 'auto-package.sh' -- "$@"`
GETOPT_RET=$?

function do_usage()
{
    cat <<EOF
Usage: $EXEC_NAME <command> [args...]
  command:
    base        Prepare base iso
    mkiso       Only make iso from iso base directory
    download    Download source code
  args:
    -h, --help  Show this help message
    -i, --iso   Input iso file, using for making base
    -o, --out   Out iso name
Example:
  $EXEC_NAME mkiso
  $EXEC_NAME base --iso=input.iso
  $EXEC_NAME mkiso --out=iso
EOF
}

if [ $GETOPT_RET != 0 ]; then
    echo "Terminating..."
    do_usage
    exit 1
fi

eval set -- "${IN_ARGS}"

ARGS_EXP=""
ARG_INPUT_ISO="input.iso"
ARG_OUT_ISO="out.iso"

while true; do
    case "$1" in
        -h|--help)
            do_usage
            exit 0
            ;;
        -i|--iso)
            ARG_INPUT_ISO="$(echo $2 | sed 's/^=//')"
            echo "[Info] In iso file: ARG_INPUT_ISO=$ARG_INPUT_ISO"
            shift 2
            ;;
        -o|--out)
            ARG_OUT_ISO="$(echo $2 | sed 's/^=//')"
            echo "[Info] Out iso file: ARG_OUT_ISO=$ARG_OUT_ISO"
            shift 2
            ;;
        --)
            shift 2
            break
            ;;
        *)
            echo "[Err] Internal error!"
            exit 1
            ;;
    esac
done
ARGS_EXP="$@"
echo "[Info] Auto package args: ARGS_EXP=$ARGS_EXP"

cd $(dirname $0)
ISO_BASE_DIR="${PWD}/iso-base"

function make_iso_base()
{
    local _input_iso=$1
    local _cdrom_dir="/mnt/iso-base"
    local _iso_base_dir=$ISO_BASE_DIR

    if [ ! -f $_input_iso ]; then
        echo "[Err] In iso is not exist..."
        exit 1
    fi

    [ -d $_iso_base_dir ] && rm -rf $_iso_base_dir
    mkdir -p $_iso_base_dir

    mount -o loog $_input_iso $_cdrom_dir

    pushd $_cdrom_dir
    tar -cvf /tmp/iso-base.tar .
    popd
    umount $_cdrom_dir
    tar -xvf /tmp/iso-base.tar -c $_iso_base_dir
    rm -rf /tmp/iso-base.tar
}

function do_mkisofs()
{
    local _iso_name=$1
    local _iso_dir=$2
    local _product_name=""
    
    mkiso/isolinux/build.sh ${_iso_dir}
    mkiso/LiveOS/build.sh ${_iso_dir}/LiveOS/squashfs.img

    # TODO: only support label 'Centos 7'
    _product_name="Centos 7"

    genisoimage -U -r -v -T -J -joliet-long -V "$_product_name x86_64" \
        -volset "$_product_name x86_64" -A "$_product_name x86_64" \
        -b isolinux/isolinux.bin -c isolinux/boot.cat\
        -no-emul-boot -boot-load-size 4 -boot-info-table -eltorito-alt-boot \
        -e images/efiboot.img -no-emul-boot -o "$_iso_name" "$_iso_dir"

    implantisomd5 $_iso_name
}

function do_download()
{
    source mkiso.conf
    local _linux_dir="${LINUX_URL$$*/}"
    if [ -d $_linux_dir ]; then
        pushd $_linux_dir
        git pull
        popd
    else
        git clone $LINUX_URL
    fi
}

if [ "X$ARGS_EXP" == "Xbase" ]; then
    make_iso_base "$ARG_INPUT_ISO"
elif [ "X$ARGS_EXP" == "Xmkiso" ]; then
    do_mkisofs "$ARG_OUT_ISO" "$ISO_BASE_DIR"
elif [ "X$ARGS_EXP" == "Xdownload" ]; then
    do_download
else
    echo "[Err] Args unknown: $ARGS_EXP"
    do_usage
fi
