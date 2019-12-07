#!/bin/bash

# Trim leading and trailing white-space from string
util_trim_string() {
    # Usage: util_trim_string "   example   string    "
    #
    # The : built-in is used in place of a temporary variable
    # The _ expands to the last argument to the previous command

    : "${1#"${1%%[![:space:]]*}"}"
    : "${_%"${_##*[![:space:]]}"}"
    printf '%s' "$_"
}

# Trim all white-space from string and truncate spaces
# shellcheck disable=SC2086,SC2048
util_trim_all() {
    # Usage: util_trim_all "   example   string    "
    set -f
    set -- $*
    printf '%s' "$*"
    set +f
}

# Use regex on a string
util_regex() {
    # Usage: util_regex "string" "regex"
    [[ $1 =~ $2 ]] && printf '%s' "${BASH_REMATCH[1]}"
}

# Change a string to lowercase
util_lower() {
    # Usage: lower "string"
    printf '%s' "${1,,}"
}

# Change a string to uppercase
util_upper() {
    # Usage: upper "string"
    printf '%s' "${1^^}"
}

# Remove duplicate array elements
util_remove_array_dups() {
    # Usage: remove_array_dups "array"
    declare -A tmp_array

    for i in "$@"; do
        [[ $i ]] && IFS=" " tmp_array["${i:- }"]=1
    done

    printf '%s ' "${!tmp_array[@]}"
}


