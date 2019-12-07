#!/bin/bash

util_trim_string() {
    # Usage: util_trim_string "   example   string    "
    #
    # The : built-in is used in place of a temporary variable
    # The _ expands to the last argument to the previous command

    : "${1#"${1%%[![:space:]]*}"}"
    : "${_%"${_##*[![:space:]]}"}"
    printf '%s' "$_"
}

