#!/usr/bin/env bash

set -e
set -o pipefail

export vmroot=$(dirname `readlink -f $0`)
[ $# -lt 2 ] && {
    if [ "X$1" != "Xlist" -a "X$1" != "Xlist_machine" ]; then
        echo "usage $0 start/stop vm" >&2
        exit 1
    fi
}

source $vmroot/scripts/common.sh

network_detect()
{
    ip link show dev br-mgmt >/dev/null 2>/dev/null || {
        echo "network not ready, pls do: '$vmroot/network_deploy.sh init' first"
        return 1
    }
}

do_startup()
{
    local name=$1

    echo "do start machine. $name..."

    # make sure user has right permission here.
    sudo ls &>/dev/null

    source $vmroot/scripts/$name.sh 2>/dev/null || {
        echo "missing config for target '$name'"
        return 0
    }

    shift
    do_start_machine $@ || {
        do_stop_machine
    }
}

do_stop()
{
    local name=$1
    echo "do stop machine. $name"

    # make sure user has right permission here.
    sudo ls &>/dev/null

    source $vmroot/scripts/$1.sh 2>/dev/null || {
        echo "missing config for target '$name'"
        return 0
    }

    shift
    do_stop_machine $@
}

do_install()
{
    local name=$1
    echo "do install machine...'$name'"
    # make sure user has right permission here.
    sudo ls &>/dev/null

    source $vmroot/scripts/$name.sh 2>/dev/null || {
        echo "missing config for target '$name'"
        return 0
    }

    shift
    do_install_machine $@
}

do_list()
{
    cd $vmroot/scripts
    ls *.sh | awk '!/^common.sh/{gsub(".sh$", "", $1); print $1}'
}

case $1 in 
    start|boot|poweron)
        shift
        network_detect
        do_startup $@
        ;;

    stop|poweroff)
        shift
        do_stop $@
        ;;

    install|start_in_cdrom|iso)
        shift
        network_detect $@
        do_install $@
        ;;

    list_machine|list)
        shift
        do_list $@
        ;;
    *)
        echo "usage: $0 start|stop|install" >&2
        exit 2
        ;;
esac
