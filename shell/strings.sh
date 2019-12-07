#!/bin/bash

test_string="1243242343"
VAR="test_string"
echo ">>>>>: ${!VAR}"

var=hello
[[ $var == hello ]] && { echo hi; echo there; } || echo bye
[[ $var1 == hello ]] && { echo hi; echo there; } || echo bye

[[ $var == hello ]] && {
    echo hi
    echo there
}

for((i=0; i<=3; i++)); do
    echo "$i"
done

test_string="http://123/456/789/aaa/b.txt"
echo ">>${test_string}"
echo ">>#*/>  ${test_string#*/}"
echo ">>##*/> ${test_string##*/}"
echo ">>%/*>  ${test_string%/*}"
echo ">>%%/*> ${test_string%%/*}"

check_string() {
    eval : "\${$1:?$1 is not set}"
}
check_string test_string
check_string "test_stringt1221" | :
