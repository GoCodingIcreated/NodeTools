#!/usr/bin/python3

import os
import sys

CONFIG = ""


if __name__ == "__main__":
    if len(sys.argv) > 1:
        CONFIG = sys.argv[1]
    os.system("openvpn --config %s" % (CONFIG))
