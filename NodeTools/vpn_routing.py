#!/usr/bin/python3

import os
import sys
import json

CONFIG = "vpn_routing_config"

if __name__ == "__main__":
    #ip = "10.8.1.0/24"
    #dev = "enp0s8"
    with open(CONFIG, "r") as file:
        data = json.load(file)
    if len(sys.argv) > 1:
        type = sys.argv[1]
    ip = data[type]["ip"]
    dev = data[type]["dev"]

    os.system("iptables -t nat -A POSTROUTING -s %s -o %s -j MASQUERADE" % (ip, dev))