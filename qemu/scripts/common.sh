#!/usr/bin/env bash

set -e
set -o pipefail

SERIAL_PORT=20000
VNC_PORT=21000
VNC_INDEX=100

serial_args()
{
    return
    # we do not use serial for now. use vnc instead
    # echo "-serial telnet:localhost:$SERIAL_PORT,server,nowait,nodelay"
}

monitor_args()
{
    echo "-monitor telnet:localhost:$VNC_PORT,server,nowait,nodelay -vnc :$VNC_INDEX"
}

qemu_common_args()
{
    if [ "X$NOGRAPHIC" == "X0" ]; then
        echo "-localtime -enable-kvm -cpu host"
    else
        echo "-nographic -localtime -enable-kvm -cpu host `serial_args` `monitor_args`"
    fi
}

qemu_machine_args()
{
    # do nothing here. which gonna be rewrite by every machine it's self
    # e.g.: cpu number, memory size..., maybe append more disks,..
    echo "-m ${MEMORY_SIZE:-512M}"
}

qemu_mirror_args()
{
   echo "-boot d -drive file=$MACHINE_MIRROR,media=cdrom"
}

do_start_one()
{
    local name=$1
    local img=$2
    local tap_br=$3
    local tap_mgmt=$4
    local tap_br_mac=$5
    local tap_mgmt_mac=$6

    [ -z $name -o -z $img -o -z $tap_br -o -z $tap_mgmt -o -z $tap_br_mac -o -z $tap_mgmt_mac ] && {
        echo "start machine failed. invalid argument. $@'" >&2
        return 1
    }

    shift 6

    cd $vmroot/vms
    img=`readlink -f $img`

    sudo qemu-system-x86_64  `qemu_common_args` \
        -name $name \
        `qemu_machine_args` \
        -drive file=$img,format=raw \
        -device ${NET_DEVICE:-"virtio-net"},netdev=vmnic_$tap_br,mac=$tap_br_mac -netdev tap,id=vmnic_$tap_br,ifname=$tap_br,script=no,downscript=no \
        -device ${NET_DEVICE:-"virtio-net"},netdev=vmnic_$tap_mgmt,mac=$tap_mgmt_mac -netdev tap,id=vmnic_$tap_mgmt,ifname=$tap_mgmt,script=no,downscript=no \
        $@ &
}

create_and_attach_tap()
{
    local tap=$1
    local br=$2

    sudo ip tuntap add mode tap $tap

    sudo ip link set dev $tap up
    sudo ip link set $tap master $br
}

detach_and_destroy_tap()
{
    local tap=$1
    local br=$2

    sudo ip link set $tap nomaster
    sudo ip link set dev $tap down
    sudo ip tuntap del mode tap $tap
}

vm_process_id()
{
    local name=$1
    ps aux | grep "qemu-system-x86_64.*$name" | grep -v -e grep -e sudo | awk '{print $2}'
}

is_vm_running()
{
    [ "X`vm_process_id $name`" != "X" ]
}

stop_vm_gracefully()
{
    local name=$1
    local retry=20

    echo "stopping vm '$name' in gracefully way..."

    echo 'system_powerdown' | nc localhost $VNC_PORT -w 5 || return 1

    while [ $retry -gt 0 ]
    do
        sleep 1
        echo -en "."

        is_vm_running $name || {
            echo "done."
            return 0
        }

        retry=`expr $retry - 1`
    done

    echo "failed. stop overtime."
    return 1
}

stop_vm_aggressive()
{
    local name=$1
    local retry=5
    local pid="`vm_process_id $name`"

    is_vm_running $name || return 0
    [ -z "$pid" ] && return 0

    echo "stopping vm '$name' pid: '$pid' in aggressive way..."

    sudo kill -INT $pid

    while [ $retry -gt 0 ]
    do
        sleep 1
        echo -en "."

        is_vm_running || {
            echo "done."
            return 0
        }

        retry=`expr $retry - 1`
    done

    echo -en "failed. try force way to kill."

    is_vm_running && {
        sudo kill -9 $pid

        is_vm_running && {
            echo "kill process $pid failed." 1>&2
            return 1
        }
    }

    echo "----------- done."

    return 0
}

do_stop_one()
{
    local $name
    stop_vm_gracefully $name || {
        stop_vm_aggressive $name || {
            echo "stop virtual machine $name failed"
        }
    }

    echo "do stop machine. done"
}

do_env_check()
{
    for key in TAP_ONE TAP_MGMT BRIDGE_X BRIDGE_MGMT MACHINE_NAME MACHINE_IMG \
        TAP_ONE_MAC TAP_MGMT_MAC \
        $@
    do
        val=$(eval "echo \$$key")

        [ -z $val ] && {
            echo "$key should be provide" >&2
            return 1
        }
    done

    return 0
}

do_start_machine()
{
    do_env_check

    create_and_attach_tap $TAP_ONE $BRIDGE_X
    create_and_attach_tap $TAP_MGMT $BRIDGE_MGMT

    do_start_one \
        $MACHINE_NAME \
        $MACHINE_IMG \
        $TAP_ONE \
        $TAP_MGMT \
        $TAP_ONE_MAC \
        $TAP_MGMT_MAC \
        $@
}

do_stop_machine()
{
    do_env_check

    do_stop_one $MACHINE_NAME

    detach_and_destroy_tap $TAP_ONE $BRIDGE_X
    detach_and_destroy_tap $TAP_MGMT $BRIDGE_MGMT
}

do_install_machine()
{
    do_env_check MACHINE_MIRROR

    create_and_attach_tap $TAP_ONE $BRIDGE_X
    create_and_attach_tap $TAP_MGMT $BRIDGE_MGMT

    # IMGS ADD HERE
    do_start_one \
        $MACHINE_NAME \
        $MACHINE_IMG \
        $TAP_ONE \
        $TAP_MGMT \
        $TAP_ONE_MAC \
        $TAP_MGMT_MAC \
        `qemu_mirror_args` \
        $@
}
