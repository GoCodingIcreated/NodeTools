#!/bin/bash


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


cd ~/openvpn-ca/keys
cp ca.crt ca.key server.crt server.key ta.key dh2048.pem /etc/openvpn

gunzip -c /usr/share/doc/openvpn/examples/sample-config-files/server.conf.gz | tee /etc/openvpn/server.conf

cat /etc/openvpn/server.conf | sed 's/;tls-auth[0-9a-zA-Z#\. ]*/tls-auth ta.key 0\nkey-direction 0/; s/;cipher AES-128-CBC/cipher AES-128-CBC\nauth SHA256/; s/;user nobody/user nobody/; s/;group/group/' > tempfile
mv tempfile /etc/openvpn/server.conf



echo "net.ipv4.ip_forward=1" >> /etc/sysctl.conf

systemctl start openvpn@server

mkdir -p ~/client-configs/files

cp /usr/share/doc/openvpn/examples/sample-config-files/client.conf ~/client-configs/base.conf

cat ~/client-configs/base.conf | sed 's/;cipher AES-128-CBC/cipher AES-128-CBC\nauth SHA256/; s/;user nobody/user nobody/; s/;group/group/; s/ca ca.crt/;ca ca.crt/; s/cert client.crt/;cert client.crt/; s/key client.key/;key client.key/' >tempfile
echo -e "\nkey-direction 1\n" >>tempfile
echo -e "\n# script-security 2\n# up /etc/openvpn/update-resolve-conf\n# down /etc/openvn/update-resolve-conf\n" >>tempfile
mv tempfile ~/client-configs/base.conf

touch ~/client-configs/make_config.sh
chmod 700 ~/client-configs/make_config.sh

echo -e "#!/bin/bash\n"\
"# First argument: Client identifier\n"\
"KEY_DIR=~/openvpn-ca/keys\n"\
"OUTPUT_DIR=~/client-configs/files\n"\
"BASE_CONFIG=~/client-configs/base.conf\n"\
"cat \${BASE_CONFIG} \ \n"\
"\t<(echo -e '<ca>') \ \n"\
"\t\${KEY_DIR}/ca.crt \ \n"\
"\t<(echo -e '</ca>\\\n<cert>') \ \n"\
"\t\${KEY_DIR}/\${1}.crt \ \n"\
"\t<(echo -e '</cert>\\\n<key>') \ \n"\
"\t\${KEY_DIR}/\${1}.key \ \n"\
"\t<(echo -e '</key>\\\n<tls-auth>') \ \n"\
"\t\${KEY_DIR}/ta.key \ \n"\
"\t<(echo -e '</tls-auth>') \ \n"\
"\t> \${OUTPUT_DIR}/\${1}.ovpn\n" >~/client-configs/make_config.sh

