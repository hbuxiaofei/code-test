#!/bin/bash

source utils.sh

test_name="   John Black  "

echo "* Before trim:>>>$test_name<<<"
ret=$(util_trim_string "$test_name")
echo "  After trim:>>>$ret<<<"

