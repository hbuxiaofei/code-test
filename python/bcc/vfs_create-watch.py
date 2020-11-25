#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
from bcc import BPF
from time import sleep
from sys import argv

def usage():
    print("USAGE: %s [time]" % argv[0])
    exit()

interval = 99999999
if len(argv) > 1:
    try:
        interval = int(argv[1])
        if interval == 0:
            raise
    except:  # also catches -h, --help
        usage()

# load BPF program
text="""
#include <uapi/linux/ptrace.h>

struct key_t {
    u64 ip;
    u32 pid;
};

BPF_PERF_OUTPUT(events);

int do_count(struct pt_regs *ctx) {
    struct key_t key = {};
    u32 pid = bpf_get_current_pid_tgid();

    key.ip = PT_REGS_IP(ctx);
    key.pid = pid;

    events.perf_submit(ctx, &key, sizeof(key));

    return 0;
}
"""
b = BPF(text=text)
b.attach_kprobe(event_re="vfs_create", fn_name="do_count")

# process event
def print_event(cpu, data, size):
    event = b["events"].event(data)
    print("%-16x %-26s %-6d" % (event.ip, b.ksym(event.ip), event.pid))

b["events"].open_perf_buffer(print_event)

# header
print("Tracing... Ctrl-C to end.")
print("\n%-16s %-26s %-6s" % ("ADDR", "FUNC", "PID"))

# output
try:
    while interval != 0:
        b.perf_buffer_poll()
        interval = interval -1
        sleep(0.1)
except KeyboardInterrupt:
    pass
