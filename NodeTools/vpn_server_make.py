#!/usr/bin/python3

import os
import sys

if __name__ == "__main__":
    ip = "10.8.1.0/24"
    dev = "enp0s8"
    if len(sys.argv) == 3:
        ip = sys.argv[1]
        dev = sys.arv[2]
    os.system("iptables -t nat -A POSTROUTING -s %s -o %s -j MASQUERADE" % (ip, dev))