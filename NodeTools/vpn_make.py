#!/usr/bin/python3

import os
import sys

config = ""

if len(sys.argv) > 1:
    config = sys.argv[1]
print(config)
os.system("openvpn --config %s" % (config))