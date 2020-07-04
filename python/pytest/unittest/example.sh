#!/bin/bash

cd $(dirname $0)
_arg="$1"

if [ "$_arg" == clean ]; then
    find ./ -name *.html | xargs rm -rf
    find ./ -name *.pyc | xargs rm -rf
    find ./ -name *.log | xargs rm -rf
    exit 0
fi

./testset/run.py
