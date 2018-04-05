#!/bin/bash


function file_exists {
    test -f $1
    return $?
}


if  ! file_exists /usr/local/bin/badvpn-tun2socks ; then
    echo "Abort : badvpn-tun2socks isn't installed"
    exit 1
fi


