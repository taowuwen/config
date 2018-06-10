#!/bin/bash

. ${HOME}/usr/bin/qemu_config 

ROOT=/home/tww/virtual_machine
TAP=tap0

start_vm()
{
	exec $QEMU \
		-localtime \
		-enable-kvm \
		-cpu host \
		-hda $ROOT/win10/win10.img \
		-m 4G \
		-net nic,vlan=0 \
		-net tap,ifname=$TAP,script=no,downscript=no \
		-monitor stdio \
		-name "win10"\
		"$@"
}

main()
{
	network_ready $TAP && start_vm $*
}

main $*



#	-net nic,vlan=0 -net tap,ifname=tap0,script=no,downscript=no
	#-net nic -net user,hostname=windowsvm \
#	-netdev user,id=network0 -device e1000,netdev=network0,mac=52:54:00:12:34:56 \
#	-net nic,macaddr=00:16:3e:00:00:04,model=virtio \
#	-drive file=$ROOT/WindowsVM.img,if=virtio \
#	-boot d -drive file=$ROOT/DEEPIN_LITEXP_SP3.iso,media=cdrom
	#-drive file=$ROOT/WindowsVM.img,if=virtio \
#DEEPIN_LITEXP_SP3.iso  gentoo.7z  sns.txt  WindowsVM.img  winxp-sn.txt
#./WindowsVM.sh -boot d -drive file=WINDOWS.iso,media=cdrom -drive file=DRIVER.iso,media=cdrom
