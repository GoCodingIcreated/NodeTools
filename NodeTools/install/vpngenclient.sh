#!/bin/bash

cd ~/openvpn-ca
source ./vars

./build-key client2
cd ~/client-configs
./make_config.sh client2
