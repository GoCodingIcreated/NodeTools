#!/bin/bash


function package_exists {
    dpkg -l "$1" &> /dev/null
    return $?
}

declare -a arr=("git" "ssh" "openvpn" "easy-rsa" "dante-server" "python3")

apt-get update
for i in "${arr[@]}"
do
    apt-get install -y $i
    if  ! package_exists $i ; then
        echo "Abort : $i can't been installed"
        exit 1
    fi
done

rm /etc/danted.conf
a = $(ifconfig | grep "eth\|enp" | head -n 1 | cut -d " " -f 1)

echo "internal: 10.0.1.1 port = 1080
external:"$a" method: username none
user.privileged: root
user.notprivileged: nobody
client pass {
	from: 0.0.0.0/0 to: 0.0.0.0/0
	log: error
}
pass {
	from: 0.0.0.0/0 to: 0.0.0.0/0
	command: connect
	log: error
	method: none
}

" > /etc/danted.conf
service danted restart
cd $HOME
mkdir badvpn-build
cd badvpn-build
git clone https://github.com/ambrop72/badvpn.git
apt-get install -y cmake
cmake ~/badvpn-build/badvpn/ -DBUILD_NOTHING_BY_DEFAULT=1 -DBUILD_TUN2SOCKS=1
make
ln -s $HOME/badvpn-build/tun2socks/badvpn-tun2socks /usr/bin/badvpn-tun2socks


