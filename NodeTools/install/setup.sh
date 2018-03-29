#!/bin/bash


function package_exists {
    dpkg -l "$1" &> /dev/null
    return $?
}

source $1

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

echo "internal: $IP_INTERNAL port = 1080
external:$IP_EXTERNAL method: username none
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
mkdir $BADVPN_PATH
cd $BADVPN_PATH
git clone https://github.com/ambrop72/badvpn.git
apt-get install -y cmake
cmake $BADVPN_PATH/badvpn/ -DBUILD_NOTHING_BY_DEFAULT=1 -DBUILD_TUN2SOCKS=1
make
rm /usr/bin/badvpn-tun2socks 2> /dev/null
ln -s $BADVPN_PATH/tun2socks/badvpn-tun2socks /usr/bin/badvpn-tun2socks


