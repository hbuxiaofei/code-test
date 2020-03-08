print.info() {
    echo "$(date +'%Y-%m-%d %H:%M:%S.%3N') ${FUNCNAME[1]}() INFO: $@" >&1
}

print.warn() {
    echo "$(date +'%Y-%m-%d %H:%M:%S.%3N') ${FUNCNAME[1]}() WARN: $@" >&2
}

print.err() {
    echo "$(date +'%Y-%m-%d %H:%M:%S.%3N') ${FUNCNAME[1]}() ERR: $@" >&2
}

print.test() {
    print.info "This is a info"
    print.warn "This is a warn"
    print.err "This is a error"
}

# print.test


