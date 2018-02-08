#!/usr/bin/env bash


gateway_info() 
{
	ip route | awk 'BEGIN {
		gw=0
		inf=0
	}
	/default/{
		for (i = 1; i < NF; i++) {
			if ($i ~ "dev") {
				i++
				inf=$i
				continue
			}

			if ($i ~ "via") {
				i++
				gw=$i
				continue
			}
		}

		exit
	}

	END {
		print inf, gw
	}
	'
}


_hostonly_net_disable()
{
	iptables -t nat -F
	iptables -t filter -F
}


_hostonly_net_enable()
{
	gwinfo=`gateway_info`

	[ -z "$gwinfo" ] && {
		echo "Network not unreachable, give up"
		exit 2
	}

	IF_S=`ip link | awk '/vboxnet[0-9]:/{gsub(":", "", $2); print $2}'`
	if_wan=`echo $gwinfo | cut -d" " -f1`
	dns_addr=`cat /etc/resolv.conf | awk '/nameserver/{print $2; eixt}'`

	[ -z "$dns_addr" -o -z "$if_wan" -o -z "$IF_S" ] && {
		echo "network not ready or dns not prepared in /etc/resolv.conf"
		exit 1
	}

	for inf in $IF_S
	do
		sysctl net.ipv4.conf.$inf.proxy_arp=1 || exit 1
	done
	sysctl net.ipv4.conf.$if_wan.proxy_arp=1 || exit 1
	sysctl net.ipv4.ip_forward=1 || exit 1

	for inf in $IF_S
	do
#		inf_addr=`ip addr show dev $inf  | awk '/inet /{gsub("/.*", "", $2); print $2}'`
#		iptables -t nat -A PREROUTING -i $inf -d $inf_addr/32 -p udp --dport 53 -j DNAT --to-destination $dns_addr:53 || exit 1
		iptables -t nat -A POSTROUTING -o $if_wan -j MASQUERADE || exit 1
		iptables -A FORWARD -i $inf -o $if_wan -m state --state RELATED,ESTABLISHED -j ACCEPT || exit 1
		iptables -A FORWARD -i $if_wan -o $inf -j ACCEPT || exit 1
	done
}


cmd="_hostonly_net_$1"

type "$cmd" &>/dev/null || {
	echo "Usage: $0 disable/enable"
	exit 1
}

shift
$cmd $*
