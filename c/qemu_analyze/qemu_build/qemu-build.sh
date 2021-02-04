#!/usr/bin/env bash

cd $(dirname $0)

BUILD_DIR="build"
CPU_NR=$(lscpu 2>/dev/null | grep "^CPU(s):" | awk '{print $2}')

install_depends4centos8() {
    ln -s /usr/bin/python3 /usr/bin/python
    yum install -y git
    yum install -y gcc
    yum install -y make

    yum install -y nettle-devel
    yum install -y glib2-devel
    yum install -y pixman-devel
    yum install -y libaio-devel
    yum install -y numactl-devel
    yum install -y libusbx-devel
    yum install -y SDL-devel
    yum install -y check-devel
    yum install -y cyrus-sasl-devel
    yum install -y libattr-devel
    yum install -y libcap-devel
    yum install -y libcurl-devel
    yum install -y libiscsi-devel
    yum install -y libjpeg-devel
    yum install -y lzo-devel
    yum install -y nss-devel
    yum install -y pciutils-devel
    yum install -y pulseaudio-libs-devel
    yum install -y rsync
    yum install -y systemtap
    yum install -y systemtap-sdt-devel
    yum install -y gnutls-devel
    yum install -y libuuid-devel
    yum install -y ncurses-devel
    yum install -y spice-server
    yum install -y spice-protocol
cat <<EOF
Please install these packages:
# rpm -ivh celt051-devel-*.rpm
# rpm -ivh spice-server-devel-*.rpm
EOF
}

print_error() {
    (echo
    echo "ERROR: $1"
    while test -n "$2"; do
        echo "       $2"
        shift
    done
    echo) >&2
}

error_exit() {
    print_error "$@"
    exit 1
}

run_cmd="git submodule init"
${run_cmd} || error_exit "${run_cmd}"

run_cmd="git submodule update"
${run_cmd} || error_exit "${run_cmd}"

if [ ! -d ${BUILD_DIR} ]; then
    mkdir -p ${BUILD_DIR}

    pushd ${BUILD_DIR}
    ../configure \
        --prefix=/usr \
        --target-list=$(uname -m 2>/dev/null)-softmmu \
        --enable-debug \
        --disable-strip \
        --enable-werror \
        --disable-slirp \
        --enable-vnc \
        --disable-docs \
        --enable-nettle \
        --enable-kvm \
        --enable-linux-aio \
        --enable-vhost-net \
        --enable-libusb \
        --enable-coroutine-pool \
        --enable-numa
    ret=$?
    popd

    if [ $ret -ne 0 ]; then
        error_exit "configure"
    fi
fi

pushd ${BUILD_DIR}
    make -j ${CPU_NR}
    ret=$?
popd

if [ $ret -ne 0 ]; then
    error_exit "make"
fi

exit 0
