#!/bin/bash

source utils.sh

print_test_error() {
    echo -e "\033[31m  [Err] Tets error: $1 ! \033[0m"
}

print_test_ok() {
    echo -e "\033[32m  [Info] Tets OK: $1 \033[0m"
}

print_test_title() {
    echo "* Test $1"
}

# Test util_trim_string
test_name="   John Black  "
echo "* Test util_trim_string"
echo "  Before trim:>>>$test_name<<<"
ret=$(util_trim_string "$test_name")
echo "  After trim:>>>$ret<<<"
if [ x"$ret" != x"John Black" ]; then
    print_test_error util_trim_string
else
    print_test_ok util_trim_string
fi

# Test util_trim_all
test_name="   I am    John   Black  "
echo "* Test util_trim_all"
echo "  Before trim all:>>>$test_name<<<"
ret=$(util_trim_all "$test_name")
echo "  After trim all:>>>$ret<<<"
if [ x"$ret" != x"I am John Black" ]; then
    print_test_error util_trim_all
else
    print_test_ok util_trim_all
fi

# Test util_regex
ret=$(util_regex '    hello' '^\s*(.*)') # Trim leading white-space.
echo "* Test util_regex"
if [ x"$ret" != x"hello" ]; then
    print_test_error util_regex
else
    print_test_ok util_regex
fi
ret=$(util_regex "#FFFFFF" '^(#?([a-fA-F0-9]{6}|[a-fA-F0-9]{3}))$') # Validate a hex color.
if [ x"$ret" != x"#FFFFFF" ]; then
    print_test_error util_regex
else
    print_test_ok util_regex
fi
ret=$(util_regex "red" '^(#?([a-fA-F0-9]{6}|[a-fA-F0-9]{3}))$') # Validate a hex color (invalid).
if [ x"$ret" != x ]; then
    print_test_error util_regex
else
    print_test_ok util_regex
fi

# Test util_lower
echo "* Test util_lower"
ret=$(util_lower "HELLO")
if [ x"$ret" != x"hello" ]; then
    print_test_error util_lower
else
    print_test_ok util_lower
fi
ret=$(util_lower "hEllO")
if [ x"$ret" != x"hello" ]; then
    print_test_error util_lower
else
    print_test_ok util_lower
fi

# Test util_upper
test_func="util_upper"
echo "* Test $test_func"
ret=$($test_func "hello")
if [ x"$ret" != x"HELLO" ]; then
    print_test_error $test_func
else
    print_test_ok $test_func
fi
ret=$($test_func "hEllO")
if [ x"$ret" != x"HELLO" ]; then
    print_test_error $test_func
else
    print_test_ok $test_func
fi

# Test util_remove_array_dups
test_func="util_remove_array_dups"
print_test_title $test_func
test_string=" 1 2 3 4 2 3 2 3 5 6 2 2 5"
ret=$($test_func $test_string)
if [ x"$ret" != x"1 2 3 4 5 6 " ]; then
    print_test_error $test_func
else
    echo "  Before remove dups >>> $test_string"
    echo "  After remove dups >>> $ret"
    print_test_ok $test_func
fi


