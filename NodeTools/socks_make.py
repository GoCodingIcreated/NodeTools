#!/usr/bin/python3

import os
import sys

if __name__ == "__main__":
    #ip_ssh = "10.0.1.1"
    username = "nickolas"
    socks_server_addr = "10.0.1.1:1080"

    ip_gw = "10.0.1.1"
    ip_virt1 = "10.0.0.1"
    netmask_virt1 = "255.255.255.0"
    ip_virt2 = "10.0.0.2"
    netmask_virt2 = "255.255.255.0"
    ip_dns = "8.8.8.8"

    tun = "tun2"

    if len(sys.argv) > 2:
        socks_server_addr = sys.argv[1]
        username = sys.argv[2]

    os.system("ip tuntap add dev %s mode tun user %s" %s (tun, username))
    os.system("ifconfig %s %s netmask %s" % (tun, ip_virt1, netmask_virt1))


    os.system("route del default")
    os.system("route add %s gw %s" % (ip_dns, ip_gw))
    os.system("route add default gw %s" % (ip_virt2))
    os.system("route -nNvee")
    print("Start tun2sock (no output):")
    os.system("badvpn-tun2socks --tundev %s --netif-ipaddr %s --netif-netmask %s --socks-server-addr %s >out" %
             (tun, ip_virt2, netmask_virt2, socks_server_addr))
    os.system("route del default")
    os.system("route add default gw %s" % (ip_gw))

