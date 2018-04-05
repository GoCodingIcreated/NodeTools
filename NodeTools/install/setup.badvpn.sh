#!/bin/bash

BADVPN_TMP_DIR=/tmp/badvpn_tmp_dir
mkdir $BADVPN_TMP_DIR
cd $BADVPN_TMP_DIR
wget https://github.com/ambrop72/badvpn/archive/1.999.130.tar.gz
tar xf *.tar.gz
cmake
cmake ./badvpn-* -DBUILD_NOTHING_BY_DEFAULT=1 -DBUILD_TUN2SOCKS=1 -DCMAKE_INSTALL_PREFIX=/usr/local
make
make install

