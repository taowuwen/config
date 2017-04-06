#!/usr/bin/env sh


#set -x
# src dst


cifs_options()
{
	# username 
	useroptions() {
		[ "$1" == "guest" ] && {
			echo "guest"
			return
		}

		echo "username=$1,password=$1"
	}


	echo "-o `useroptions $1`,uid=1000,gid=1000,file_mode=0640,dir_mode=0750,iocharset=utf8"
}

usb_options()
{
	echo "-o uid=1000,gid=1000,umask=0,fmask=0137,dmask=0022,codepage=936,utf8=1,iocharset=utf8"
}


_do_mount()
{
	mount -t cifs //10.0.12.5/$1 $2 `cifs_options $3`
}

mount_public()
{
	_do_mount public ./10_5_public guest
}

mount_fitap()
{
	_do_mount fitap ./10_5_fitap fitap
}

mount_fatap()
{
	_do_mount fatap ./10_5_fatap fatap
}


mount_usb()
{
	mount $* `usb_options`
}

main()
{
	case $1 in
		public)
			mount_public
		;;


		fitap)
			mount_fitap
		;;

		fatap)
			mount_fatap
		;;

		all)
			mount_public
			mount_fitap
			mount_fatap
		;;

		usb)
			shift
			mount_usb $*
		;;

		smb)
			shift
			mount $* `cifs_options`
		;;
		
		cdrom)
			shift
			mount_cdrom $*
		;;

		umount)
			umount /home/tww/share_net/10_5_public &>/dev/null
			umount /home/tww/share_net/10_5_fitap  &>/dev/null
			umount /home/tww/share_net/10_5_fatap  &>/dev/null
			umount /home/tww/share_net/usb  &>/dev/null
			umount /home/tww/share_net/cdrom  &>/dev/null
			umount /home/tww/share_net/27  &>/dev/null
		;;

		*)
			echo "Usage: $0 incoming/public/all/umount/usb/smb"
		;;
	esac
}


main $*
exit $?
