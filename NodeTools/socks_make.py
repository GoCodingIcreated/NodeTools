#!/usr/bin/python3

import os
import sys
import time
import json
CONFIG = "socks_make_config.json"

if __name__ == "__main__":
    if len(sys.argv) > 1:
        CONFIG = sys.argv[1]

    with open(CONFIG, "r") as file:
        data = json.load(file)

    username = data["username"]
    socks_server_addr = data["socks_server_addr"]

    ip_gw = data["ip_gw"]
    ip_virt1 = data["ip_virt1"]
    netmask_virt1 = data["netmask_virt1"]
    ip_virt2 = data["ip_virt2"]
    netmask_virt2 = data["netmask_virt2"]
    ip_dns = data["ip_dns"]
    tun = data["tun"]

    if len(sys.argv) == 4:
        socks_server_addr = sys.argv[2]
        username = sys.argv[3]

    os.system("ip tuntap add dev %s mode tun user %s" % (tun, username))
    os.system("ifconfig %s %s netmask %s" % (tun, ip_virt1, netmask_virt1))

    time.sleep(1)
    pid = os.fork()
    if pid == 0:
        # child
        print("Start tun2sock (no output):")
        os.system("badvpn-tun2socks --tundev %s --netif-ipaddr %s --netif-netmask %s --socks-server-addr %s >out" %
                  (tun, ip_virt2, netmask_virt2, socks_server_addr))
    else:
        time.sleep(1)
        os.system("route del default")
        os.system("route add %s gw %s" % (ip_dns, ip_gw))
        os.system("route add default gw %s  device %s" % (ip_virt2, tun))
        os.system("route -nNvee")
        try:
            os.wait()
        except KeyboardInterrupt:
            pass
        os.system("route del default")
        os.system("route add default gw %s" % (ip_gw))
        os.system("ifconfig %s down" % (tun))

