#!/bin/sh

apt-get update
apt-get install -y git
apt-get install -y ssh

apt-get install -y dante-server
rm /etc/danted.conf
echo "internal: 10.0.1.1 port = 1080
external: eth0 
method: username none
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

mkdir badvpn-build
cd badvpn-build
git clone https://github.com/ambrop72/badvpn.git
apt-get install -y cmake
cmake ~/badvpn-build/badvpn/ -DBUILD_NOTHING_BY_DEFAULT=1 -DBUILD_TUN2SOCKS=1
make
ln -s /home/ubuntu/badvpn-build/tun2socks/badvpn-tun2socks /usr/bin/badvpn-tun2socks


