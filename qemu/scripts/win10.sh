
export SERIAL_PORT=7001
export VNC_PORT=7101
export VNC_INDEX=1

export TAP_ONE=tap1
export TAP_MGMT=tap21

export TAP_ONE_MAC=52:54:00:12:34:01
export TAP_MGMT_MAC=52:54:00:12:34:21

export BRIDGE_X=br0
export BRIDGE_MGMT=br-mgmt
export MACHINE_NAME=win10
export MACHINE_IMG=win10.img
export MEMORY_SIZE=4G

# export NOGRAPHIC=0
export NET_DEVICE=e1000

#export MACHINE_MIRROR=/home/vantron/data/software/cn_windows_10_business_editions_version_20h2_x64_dvd_f978664f.iso
export MACHINE_MIRROR=/home/vantron/data/software/SW_DVD5_Win_Pro_7w_SP1_64BIT_ChnSimp_-2_MLF_X17-59526.ISO

qemu_machine_args()
{
    echo "-m $MEMORY_SIZE -smp 4"
}
