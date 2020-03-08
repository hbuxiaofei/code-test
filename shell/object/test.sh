#!/bin/bash
. bash/libbase.sh

import bash:libobject
import bash:pkgprint

# print
echo "test print level message..."
print.test


echo ""
echo "test class..."
# class definition
class Storpel
    var name
    var quality
    func Storpel
    func set_name
    func set_quality
    func print_info

# class implementation
Storpel::Storpel() {
    set_name "$1"
    set_quality "$2"
    if [ -z "$name" ]; then set_name "Generic"; fi
    if [ -z "$quality" ]; then set_quality "Normal"; fi
}

Storpel::set_name() {
    name="$1"
}

Storpel::set_quality()
{
    quality="$1"
}

Storpel::print_info()
{
    echo "$name ($quality)"
}

test_class() {
    # usage
    new Storpel one "xiaoming" "Medium"
    new Storpel two
    new Storpel three

    two.set_name "xiaoli"
    two.set_quality "Strong"
    three.set_name "xiaohong"

    one.print_info
    two.print_info
    three.print_info

    echo "one: $one ($(typeof $one))"
    echo "two: $two ($(typeof $two))"
    echo "three: $three ($(typeof $two))"
}

test_class
