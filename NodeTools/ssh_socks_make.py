#!/usr/bin/python3

import os
import sys

if __name__ == "__main__":
    ip_ssh = "10.0.1.1"
    username = "nickolas"

    ip_gw = "10.0.1.1"
    ip_virt1 = "10.0.0.1"
    netmask_virt1 = "255.255.255.0"
    ip_virt2 = "10.0.0.2"
    netmask_virt2 = "255.255.255.0"
    ip_dns = "8.8.8.8"

    socks_server_addr = "localhost:1080"

    if len(sys.argv) > 2:
        ip_ssh = sys.argv[1]
        username = sys.argv[2]

    os.system("ip tuntap add dev tun3 mode tun user %s" % username)
    os.system("ifconfig tun3 %s netmask %s" % (ip_virt1, netmask_virt1))

    pid = os.fork()

    if pid != 0:
        # parent
        os.system("badvpn-tun2socks --tundev tun0 --netif-ipaddr %s --netif-netmask %s --socks-server-addr %s >out" %
                 (ip_virt2, netmask_virt2, socks_server_addr))
    else:
        #child
        #os.system("route add %s gw %s" % (ip_ssh, ip_gw))
        os.system("route del default")
        os.system("route add %s gw %s" % (ip_dns, ip_gw))
        os.system("route add default gw %s" % (ip_virt2))
        os.system("route -nNvee")
        os.system("ssh -l %s -D %s %s" % (username, socks_server_addr, ip_ssh))

        os.system("route del default")
        os.system("route add default gw %s" % (ip_gw))