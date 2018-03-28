#!/bin/bash

PASSWORD='123123123'

apt-get update
apt-get install -y openvpn easy-rsa 

make-cadir ~/openvpn-ca
chmod 777 ~/openvpn-ca
cd ~/openvpn-ca
cat vars | sed 's/KEY_NAME="[a-zA-Z0-9]*"/KEY_NAME="server"/' >tempfile
mv tempfile vars

cd ~/openvpn-ca/
source ./vars

./clean-all
yes '' | ./build-ca


./build-key-server --batch server

./build-dh

openvpn --genkey --secret keys/ta.key

cd ~/openvpn-ca
source ./vars
./build-key --batch client1

#no need ?
#cd ~/openvpn-ca
#source ./vars
#echo -e $PASSWORD'\n'$PASSWORD'\n' | ./build-key-pass --batch client1


cd ~/openvpn-ca/keys
sudo cp ca.crt ca.key server.crt server.key ta.key dh2048.pem /etc/openvpn

gunzip -c /usr/share/doc/openvpn/examples/sample-config-files/server.conf.gz | sudo tee /etc/openvpn/server.conf

cat /etc/openvpn/server.conf | sed 's/;tls-auth[0-9a-zA-Z#\. ]*/tls-auth ta.key 0\nkey-direction 0/; s/;cipher AES-128-CBC/cipher AES-128-CBC\nauth SHA256/; s/;user nobody/user nobody/; s/;group/group/' > tempfile
mv tempfile /etc/openvpn/server.conf


# decomment /etc/openvpn/server.conf

echo "net.ipv4.ip_forward=1" >> /etc/sysctl.conf

sudo systemctl start openvpn@server

mkdir -p ~/client-configs/files

cp /usr/share/doc/openvpn/examples/sample-config-files/client.conf ~/client-configs/base.conf

cat ~/client-configs/base.conf | sed 's/;cipher AES-128-CBC/cipher AES-128-CBC\nauth SHA256/; s/;user nobody/user nobody/; s/;group/group/' >tempfile
echo \n"key-direction 1"\n >>tempfile
mv tempfile ~/client-configs/base.conf
