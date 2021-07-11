#!/usr/bin/python

# HOW TO USE
#
# Copy this file to libvirt daemon hook
# cp -f libvirt_hook_daemon.py /etc/libvirt/hooks/daemon

import os
import sys
import json
import datetime
import socket
import shutil


MSG_TYPE_EVENT = "event"

MSG_SENDER_LIBVIRTD = "libvirtd"

LOG_FILE_PATH = "/var/log/libvirt-hook-daemon.log"

# Start a unix socket server for debug.
#
# nc -Uv -lk /var/run/vm-agent/vm-agent.sock
#   -U, --unixsock             Use Unix domain sockets only
#   -v, --verbose              Set verbosity level (can be used several times)
#   -l, --listen               Bind and listen for incoming connections
#   -k, --keep-open            Accept multiple connections in listen mode
#
SOCK_VM_AGENT = "/var/run/vm-agent/vm-agent.sock"

SOCK_LIBVIRTD = "/var/run/libvirt"


class Message(object):
    def __init__(self, msg_type, msg_sender):
        self._type = msg_type
        self._sender = msg_sender
        self._data = None

    def set_data(self, msg_data):
        self._data = msg_data

    def format_json(self):
        msg_dict = {}
        msg_dict["type"] = self._type
        msg_dict["sender"] = self._sender
        msg_dict["data"] = self._data
        return json.dumps(msg_dict)


class MessageEventLibvirt(Message):
    def __init__(self):
        # for python3
        # super().__init__(MSG_TYPE_EVENT, MSG_SENDER_LIBVIRTD)

        # for python2
        super(MessageEventLibvirt, self).__init__(MSG_TYPE_EVENT, MSG_SENDER_LIBVIRTD)

        self._container = None

    def set_container_name(self, container_name):
        self._container = container_name

    def format_json(self):
        msg_dict = {}
        msg_dict["type"] = self._type
        msg_dict["sender"] = self._sender
        msg_dict["data"] = self._data
        msg_dict["container"] = self._container
        return json.dumps(msg_dict)


def log_out(out, line_feed=True, file_path=None):
    if file_path is None:
        file_path = LOG_FILE_PATH
    try:
        fd = open(file_path, "a+")
        if line_feed:
            fd.write("%s\n" % out)
        else:
            fd.write("%s" % out)
    finally:
        if fd:
            fd.close()


def get_localtime():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")


def log_info(out, line_feed=True):
    time_string = get_localtime()
    msg_string = "[Info] [%s] %s" % (time_string, out)
    log_out(msg_string)


def log_warn(out, line_feed=True):
    time_string = get_localtime()
    msg_string = "[Warn] [%s] %s" % (time_string, out)
    log_out(msg_string)


def log_err(out, line_feed=True):
    time_string = get_localtime()
    msg_string = "[Err ] [%s] %s" % (time_string, out)
    log_out(msg_string)


def get_container_name():
    cgroup_file = "/proc/self/cgroup"

    first_line = ""
    container_name = "0" * 12
    try:
        fd = open(cgroup_file, "r")
        # read the first line only
        first_line = fd.readline()
    finally:
        if fd:
            fd.close()

    log_info(first_line)

    array = first_line.strip().split("/")

    if len(array) >= 3:
        # 12:cpuset:/docker/9440dd89c4052167611e467efd47e1feccabaad448594cbc90eb7fb3f12f4c3f
        if array[1] == "docker":
            container_name = array[2][0:11]

    log_info("container name: %s" % container_name)
    return container_name


def get_container_dir():
    vmagent_dir = os.path.dirname(SOCK_VM_AGENT)
    container_name = get_container_name()

    container_dir = ""
    if len(container_name):
        # /var/run/vm-agent/000000000000/
        container_dir = os.path.join(vmagent_dir, container_name)
    return container_dir


def unix_socket_send(message):
    sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    if sock < 0:
        log_err("socket error: %s" % sys.stderr)
        return False

    try:
        sock.connect(SOCK_VM_AGENT)
        sock.sendall(message)
    except socket.error:
        log_err("socket send error: %s" % sys.stderr)
        return False
    return True


def create_container_dir():
    # /var/run/vm-agent/000000000000/
    container_dir = get_container_dir()
    if len(container_dir):
        if not os.path.exists(container_dir):
            log_info("create %s" % container_dir)
            os.makedirs(container_dir)
    else:
        log_err("error to get container directory")
        sys.exit(1)


def create_symlink_libvirt():
    src = SOCK_LIBVIRTD
    dst = ""

    # /var/run/vm-agent/000000000000/var/run/libvirt
    container_dir = get_container_dir()
    if len(container_dir) and os.path.exists(container_dir):
        dst = os.path.join(container_dir, "libvirt")
    else:
        log_err("join symlink destination err, container directory %s error" % container_dir)

    try:
        log_info("symlink %s %s" % (src, dst))
        os.symlink(src, dst)
    except OSError as e:
        log_err("symlink %s %s, %s" % (src, dst, e))


def remove_container_dir():
    # /var/run/vm-agent/000000000000/
    container_dir = get_container_dir()
    if len(container_dir):
        if os.path.exists(container_dir):
            log_info("remove %s" % container_dir)
            shutil.rmtree(container_dir)
    else:
        log_err("error to get container directory")
        sys.exit(1)


def notify_msg(action):
    msg = MessageEventLibvirt()
    msg.set_data("%s" % action)
    msg.set_container_name("%s" % get_container_name())
    json_message = msg.format_json()

    log_info(json_message)
    unix_socket_send(json_message)


def run():
    if len(sys.argv) < 2:
        return

    vmagent_dir = os.path.dirname(SOCK_VM_AGENT)
    if not os.path.exists(vmagent_dir):
        log_err("%s not exist" % vmagent_dir)
        sys.exit(1)

    #  script_name = sys.argv[0]
    #  input1 = sys.argv[1]
    action = sys.argv[2]

    if action == "start":
        # 1. create container directory
        create_container_dir()
        # 2. create libvirt sock symlink
        create_symlink_libvirt()
        # 3. notify start
        notify_msg(action)
    elif action == "shutdown":
        # 1. notify shutdown
        notify_msg(action)
        # 2. remove container directory
        remove_container_dir()
    else:
        # only notify
        notify_msg(action)


if __name__ == "__main__":
    run()
    sys.exit(0)
