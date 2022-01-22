
export SERIAL_PORT=7000
export VNC_PORT=7100
export VNC_INDEX=0

export TAP_ONE=tap0
export TAP_MGMT=tap20
export TAP_ONE_MAC=52:54:00:12:34:00
export TAP_MGMT_MAC=52:54:00:12:34:20

export BRIDGE_X=br0
export BRIDGE_MGMT=br-mgmt
export MACHINE_NAME=suse15sp3
export MACHINE_IMG=suse15sp3.img
export MEMORY_SIZE=1G

qemu_machine_args()
{
    # do not support as follow line.
    # echo "-m $MEMORY_SIZE -smp sockets=1,cores=2,threads=2,maxcpus=4"
    # qemu-system-x86_64: AMD CPU doesn't support hyperthreading. Please configure -smp options properly.

    # use this.
    echo "-m $MEMORY_SIZE -smp 4"
}
