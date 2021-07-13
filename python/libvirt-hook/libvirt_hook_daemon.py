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
# nc -Uv -lk /var/run/node-agent/node-agent.sock
#   -U, --unixsock             Use Unix domain sockets only
#   -v, --verbose              Set verbosity level (can be used several times)
#   -l, --listen               Bind and listen for incoming connections
#   -k, --keep-open            Accept multiple connections in listen mode
#
SOCK_AGENT = "/var/run/node-agent/node-agent.sock"

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
        super().__init__(MSG_TYPE_EVENT, MSG_SENDER_LIBVIRTD)

        # for python2
        # super(MessageEventLibvirt, self).__init__(MSG_TYPE_EVENT, MSG_SENDER_LIBVIRTD)

        self._containerid = None
        self._hostname = socket.gethostname()

    def set_container_id(self, container_id):
        self._containerid = container_id

    def format_json(self):
        msg_dict = {}
        msg_dict["type"] = self._type
        msg_dict["sender"] = self._sender
        msg_dict["data"] = self._data
        msg_dict["containerid"] = self._containerid
        msg_dict["hostname"] = self._hostname
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


def get_container_id():
    cgroup_file = "/proc/self/cgroup"

    container_id = "0" * 12
    try:
        fd = open(cgroup_file, "r")

        # 9:cpuset:/kubepods.slice/kubepods-burstable.slice/
        #    kubepods-burstable-pod58764839_cf99_4c53_8936_01af3bf2b93e.slice/
        #    docker-1ed3cb9db7df02ef112c8260110f12b5833f0542c8a138b2eea60271a4184ee0.scope
        while True:
            line = fd.readline()
            if line:
                log_info(line)
                line_array = line.strip().split("docker-")
                if len(line_array) < 2:
                    continue
                container_id = line_array[-1][:12]
                break
            else:
                break
    finally:
        if fd:
            fd.close()

    log_info("container id: %s" % container_id)
    return container_id


def get_container_dir():
    agent_dir = os.path.dirname(SOCK_AGENT)
    container_id = get_container_id()

    container_dir = ""
    if len(container_id):
        # /var/run/node-agent/000000000000/
        container_dir = os.path.join(agent_dir, container_id)
    return container_dir


def unix_socket_send(message):
    try:
        sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        sock.connect(SOCK_AGENT)
        sock.sendall(message)
    except socket.error:
        log_err("socket send error: %s" % sys.stderr)
        return False
    return True


def create_container_dir():
    # /var/run/node-agent/000000000000/
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

    # /var/run/node-agent/000000000000/var/run/libvirt
    container_dir = get_container_dir()
    if len(container_dir) and os.path.exists(container_dir):
        dst = os.path.join(container_dir, "libvirt")
    else:
        log_err("join symlink destination err, container directory %s error" % container_dir)

    try:
        log_info("symlink %s %s" % (src, dst))
        if os.path.exists(dst):
            if os.readlink(dst) != src:
                shutil.rmtree(dst)
                os.symlink(src, dst)
            else:
                log_info("symlink %s to %s already exist" % (src, dst))
        else:
            os.symlink(src, dst)
    except OSError as e:
        log_err("symlink %s %s, %s" % (src, dst, e))


def remove_container_dir():
    # /var/run/node-agent/000000000000/
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
    msg.set_container_id("%s" % get_container_id())
    json_message = msg.format_json()

    log_info(json_message)
    unix_socket_send(json_message)


def run():
    if len(sys.argv) < 2:
        return

    agent_dir = os.path.dirname(SOCK_AGENT)
    if not os.path.exists(agent_dir):
        log_err("%s not exist" % agent_dir)
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
