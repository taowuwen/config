#!/usr/bin/env bash

set -e
set -o pipefail

do_sudo()
{
    echo $@ >&2
    sudo $@
}

deploy_mgmt()
{
    do_sudo ip link add br-mgmt type bridge
    do_sudo ip link set dev br-mgmt up
    do_sudo ip addr add 10.0.13.1/24 dev br-mgmt 
}

deploy_br0()
{
    do_sudo ip link add br0 type bridge
    do_sudo ip link set dev br0 up
    do_sudo ip addr add 10.0.12.1/24 dev br0
}

deploy_br_net()
{
    do_sudo ip link add br-net type bridge
    do_sudo ip link set dev br-net up
    
    # network namespace here
    do_sudo ip netns add net1
    do_sudo ip link set enp7s0 netns net1

    do_sudo ip netns exec net1 ip link add br-net type bridge
    do_sudo ip netns exec net1 ip link set enp7s0 master br-net

    # add veth
    do_sudo ip link add veth0 type veth peer name veth1

    # link veth0 to outter br-net
    do_sudo ip link set veth0 master br-net

    # link veth1 to inner br-net
    do_sudo ip link set veth1 netns net1
    do_sudo ip netns exec net1 ip link set veth1 master br-net

    # link up
    do_sudo ip link set dev veth0 up

    do_sudo ip netns exec net1 ip link set dev br-net up
    do_sudo ip netns exec net1 ip link set dev enp7s0 up
    do_sudo ip netns exec net1 ip link set dev veth1 up
}

undeploy_mgmt()
{
    do_sudo ip link set dev br-mgmt down

    # clear br-mgmt
    do_sudo ip -br link show master br-mgmt | awk '{gsub("@.*", "", $1); print $1}' |
    while read dev
    do
        do_sudo ip link set $dev nomaster
    done

    do_sudo ip link del dev br-mgmt
}

undeploy_br0()
{
    do_sudo ip link set dev br0 down

    # clear br0
    do_sudo ip -br link show master br0 | awk '{gsub("@.*", "", $1); print $1}' |
    while read dev
    do
        do_sudo ip link set $dev nomaster
    done

    do_sudo ip link del dev br0
}

undeploy_br_net()
{
    do_sudo ip netns exec net1 ip link set dev br-net down

    # clear inner br-net
    do_sudo ip netns exec net1 ip -br link show master br-net | awk '{gsub("@.*", "", $1); print $1}' |
    while read dev
    do
        do_sudo ip netns exec net1 ip link set $dev nomaster
    done

    # delete inner br-net
    do_sudo ip netns exec net1 ip link del dev br-net

    # move out all the inf from netns
    do_sudo ip netns exec net1 ip -br link  | awk '!/lo/{gsub("@.*", "", $1); print $1}' |
    while read dev
    do
        do_sudo ip netns exec net1 ip link set $dev netns 1
    done

    # delete net1
    do_sudo ip netns del net1

    # clear outter br-net
    do_sudo ip -br link show master br-net | awk '{gsub("@.*", "", $1); print $1}' |
    while read dev
    do
        do_sudo ip link set $dev nomaster
    done

    # delete veth pair
    do_sudo ip link del veth0

    # delete outter bridge
    do_sudo ip link del dev br-net
}

deploy_firewall()
{
    # we permit br0 do nat and cross firewall only
    sudo sysctl net.ipv4.ip_forward=1

    # arp proxy? not handle for currently.
    sudo iptables -t nat -A POSTROUTING -s 10.0.12.0/24 -o enp6s0 -j MASQUERADE

    # since that the default rule for FORWARD is ACCEPT
    # sudo iptables -A FORWARD -i enp6s0 -o br0 -m state --state RELATED,ESTABLISHED -j ACCEPT
    # br-net? that's another gateway's task
}

undeploy_firewall()
{
    sudo sysctl net.ipv4.ip_forward=0

    # arp proxy? not handle for currently.
    sudo iptables -t nat -D POSTROUTING -s 10.0.12.0/24 -o enp6s0 -j MASQUERADE
}

# br-br1
do_deploy() {
    deploy_mgmt
    deploy_br0
    deploy_br_net

    deploy_firewall
}

do_undeploy() {
    undeploy_firewall

    undeploy_mgmt
    undeploy_br0
    undeploy_br_net
}

case $1 in 
    init|deploy)
        do_deploy $@
        ;;

    uninit|undeploy)
        do_undeploy $@
        ;;

    * )
        echo "usage: $0 init/uninit" 1>&2
        exit 1
        ;;
esac

