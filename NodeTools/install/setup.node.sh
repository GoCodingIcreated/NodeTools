#!/bin/bash


function package_exists {
    dpkg -l "$1" &> /dev/null
    return $?
}


declare -a arr=("git" "ssh" "openvpn" "easy-rsa" "dante-server" "python3" "cmake")

#apt-get update
for i in "${arr[@]}"
do
    apt-get install -y $i
    if  ! package_exists $i ; then
        echo "Abort : $i can't been installed"
        exit 1
    fi
done


./setup.badvpn.sh
./setup.socks.sh $1
./setup.ssh.sh
./setup.vpn.sh $1
