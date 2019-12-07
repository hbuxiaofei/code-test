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

# Generate a UUID V4
# The generated value is not cryptographically secure.
util_uuid() {
    # Usage: util_uuid
    C="89ab"

    for ((N=0;N<16;++N)); do
        B="$((RANDOM%256))"

        case "$N" in
            6)  printf '4%x' "$((B%16))" ;;
            8)  printf '%c%x' "${C:$RANDOM%${#C}:1}" "$((B%16))" ;;

            3|5|7|9)
                printf '%02x-' "$B"
            ;;

            *)
                printf '%02x' "$B"
            ;;
        esac
    done
}

# Progress bars
util_bar() {
    # Usage: bar 1 10
    #            ^----- Elapsed Percentage (0-100).
    #               ^-- Total length in chars.
    ((elapsed=$1*$2/100))

    # Create the bar with spaces.
    printf -v prog  "%${elapsed}s"
    printf -v total "%$(($2-elapsed))s"

    printf '%s\r%3s%% ' "[${prog// /-}${total}]" $i
}


# Run a command in the background
# This will run the given command and keep it running,
# even after the terminal or SSH connection is terminated.
# All output is ignored.
util_bkr() {
    # Usage util_bkr ./some_script.sh
    (nohup "$@" &>/dev/null &)
}

# Display an error if empty or unset.
util_set_check() {
    # Usage: util_set_check var
    eval : "\${$1:?$1 is not set}"
}
