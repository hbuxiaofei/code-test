#!/usr/bin/env bash

DEFAULT_VSWITCH="ns-vswitch"

# terminal color define
c_nc='\e[0m'       # 没有颜色
c_red='\e[1;31m'   # 红色
c_green='\e[1;32m' # 绿色


_is_number()
{
	if [ $1 -ge 0 ] >/dev/null 2>&1; then
        return 0
	else
        return 1
	fi
}


create_example()
{
    ip netns add ns0
    ip netns add ns1
    ip netns add ns2

    ip link add type veth
    ip link add type veth
    ip link add type veth

    ip link set veth0 netns ns0
    ip link set veth2 netns ns1
    ip link set veth4 netns ns2

    # ip netns exec ns0 /bin/bash --rcfile <(echo "PS1=\"ns0> \"")
    # ns0> ip addr add 10.0.0.1/24 dev veth0
    # ns0> ip link set veth0 up
    ip netns exec ns0 ip addr add 10.0.0.1/24 dev veth0
    ip netns exec ns0 ip link set veth0 up


    # ip netns exec ns1 /bin/bash --rcfile <(echo "PS1=\"ns1> \"")
    # ns1> ip addr add 10.0.0.2/24 dev veth2
    # ns1> ip link set veth2 up
    ip netns exec ns1 ip addr add 10.0.0.2/24 dev veth2
    ip netns exec ns1 ip link set veth2 up

    # ip netns exec ns2 /bin/bash --rcfile <(echo "PS1=\"ns2> \"")
    # ns2> ip addr add 10.0.0.3/24 dev veth4
    # ns2> ip link set veth4 up
    ip netns exec ns2 ip addr add 10.0.0.3/24 dev veth4
    ip netns exec ns2 ip link set veth4 up


    ovs-vsctl add-br vswitch0
    ovs-vsctl add-port vswitch0 veth1
    ovs-vsctl add-port vswitch0 veth3
    ovs-vsctl add-port vswitch0 veth5

    ip link set dev veth1 up
    ip link set dev veth3 up
    ip link set dev veth5 up
}


# namespace name: ns-$1
# vlan: $2
create_ns_witch_veth()
{
    local _suffix="$1"
    local _vlan="$2"

    local _ns=""
    local _veth0=""
    local _veth1=""

    if ! _is_number "$_suffix" ; then
        echo -e "${c_red}[Err]${c_nc} network namespace suffix must be a number(not zero)!"
        return 1
    fi

    if [ $_suffix -eq 0 ] ; then
        echo -e "${c_red}[Err]${c_nc} network namespace suffix could not be a zero!"
        return 1
    fi

    if [ -n "$_vlan" ]; then
        if ! _is_number "$_vlan" ; then
            echo -e "${c_red}[Err]${c_nc} vlan must be a number(not zero)!"
            return 1
        fi

        if [ $_vlan -eq 0 ] ; then
            echo -e "${c_red}[Err]${c_nc} vlan could not be a zero!"
            return 1
        fi
    fi

    _ns="ns$_suffix"
    _veth0="ns-veth${_suffix}"
    _veth1="veth${_suffix}"

    ip netns add ${_ns}
    ip link add ${_veth0} type veth peer name ${_veth1}
    ip link set ${_veth0} netns ${_ns}
    ip netns exec ${_ns} ip addr add 10.0.0.${_suffix}/24 dev ${_veth0}
    ip netns exec ${_ns} ip link set ${_veth0} up

    if ! ovs-vsctl br-exists $DEFAULT_VSWITCH; then
        ovs-vsctl add-br $DEFAULT_VSWITCH
    fi

    ovs-vsctl add-port $DEFAULT_VSWITCH ${_veth1}
    ovs-vsctl set port ${_veth1} tag=${_vlan}
    ip link set dev ${_veth1} up

    echo -e "${c_green}[Info]${c_nc} create $_ns successfully, you may run:"
    # ip netns exec ns /bin/bash --rcfile <(echo "PS1=\"ns> \"")
    echo -n "ip netns exec "
    echo -n "${_ns} "
    echo -n '/bin/bash --rcfile <(echo "PS1=\"'
    echo -n "${_ns} "
    echo '> \"")'
}

# ns name: ns-$1
delete_ns_witch_veth()
{
    local _suffix="$1"
    local _ns=""
    local _veth0=""
    local _veth1=""

    if ! _is_number "$_suffix" ; then
        echo "[Err] network namespace suffix must be a number(not zero)!"
        return 1
    fi

    if [ $_suffix -eq 0 ] ; then
        echo "[Err] network namespace suffix could not be a zero!"
        return 1
    fi

    _ns="ns${_suffix}"
    _veth0="ns-veth${_suffix}"
    _veth1="veth${_suffix}"

    ip netns del ${_ns}
    ip link del ${_veth0} 2>/dev/null
    ip link del ${_veth1} 2>/dev/null

    if ovs-vsctl br-exists $DEFAULT_VSWITCH; then
        ovs-vsctl del-port $DEFAULT_VSWITCH ${_veth0} 2>/dev/null
        ovs-vsctl del-port $DEFAULT_VSWITCH ${_veth1} 2>/dev/null
    fi

}

exit 0

create_ns_witch_veth 121 100
create_ns_witch_veth 122 100
create_ns_witch_veth 123 100

exit 0

delete_ns_witch_veth 121
delete_ns_witch_veth 122
delete_ns_witch_veth 123

exit 0


