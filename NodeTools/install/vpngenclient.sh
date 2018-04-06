#!/bin/bash

source $1

cd $OPENVPN_CA_DIR
source ./vars

./build-key --batch $CLIENT_CONFIG_NAME
cd $OPENVPN_CLIENT_CONFIG_DIR
./make_config.sh $CLIENT_CONFIG_NAME
