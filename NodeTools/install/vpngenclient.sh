#!/bin/bash

source $1

cd $OPENVPN_CA_DIR
source ./vars

./build-key client2
cd $OPENVPN_CLIENT_CONFIG_DIR
./make_config.sh client2
