#!/usr/bin/env bash

cd $(dirname $0)

./helper self install && {
    cat << EOF
Install helper successfully! You can run as below.

EOF
    ./helper --help
}

exit 0
