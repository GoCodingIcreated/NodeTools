#!/usr/bin/python3

import paramiko
import time


class SSHConnection(object):
    def __init__(self, host, login, password, port):
        self.host = host
        self.login = login
        self.password = password
        self.port = int(port)
        self.client = None
        self.channel = None

    def CreateSSHConnection(self):
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(hostname=self.host, username=self.login,
                       password=self.password, port=self.port)
        self.client = client



    def CloseSSHConnection(self):
        self.channel.close()
        self.client.close()

    def ExecCommand(self, command):
        if (command.startswith('sudo')):
            self.SudoCommand(command)
        stdin, stdout, stderr = self.client.exec_command(command)
        print(stdout.read().decode('utf-8'))

    def SudoCommand(self, command):
        channel = self.client.get_transport().open_session()
        channel.get_pty()
        channel.settimeout(100)

        channel.exec_command(command)
        out = channel.recv(1024)
        print(out)
        channel.send(self.password + "\n")
        time.sleep(1)
        out = ""
        while True:
            newout = channel.recv(1024)
            print(newout.decode('utf-8'), end="")
            if newout == b'':
                break;

        channel.close()
        print( out)
        return out

    def ExecSSHSocksMakeScript(self, command):
        channel = self.client.get_transport().open_session()
        channel.get_pty()
        channel.settimeout(100)

        channel.exec_command(command)
        out = channel.recv(10240)
        print(out)
        print("Z")
        channel.send(self.password + "\n")

        print("C")
        time.sleep(1)
        print("A")
        out = channel.recv(10240)
        print(out.decode('utf-8'))
        print("X")
        channel.send(self.password + "\n")
        time.sleep(2)
        print("B")
        out = channel.recv(10240)
        #channel.close()
        print("C")
        print(out.decode('utf-8'))
        return channel

    def ExecVPNMake(self, command):
        channel = self.client.get_transport().open_session()
        channel.get_pty()
        channel.settimeout(100)

        channel.exec_command(command)
        out = channel.recv(10240)
        print(out)
        print("Z")
        channel.send(self.password + "\n")

        print("C")
        time.sleep(1)

        out = channel.recv(10240)
        print(out.decode('utf-8'))

        return channel


import argparse
import sys

def CreateParser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-H', '--hostname')
    parser.add_argument('-L', '--login')
    parser.add_argument('-P', '--password')
    parser.add_argument('-p', '--port')
    return parser
 

if __name__ == '__main__':
    parser = CreateParser()
    namespace = parser.parse_args(sys.argv[1:])
    host, login, password, port = (namespace.hostname,
                                   namespace.login,
                                   namespace.password,
                                   namespace.port)
    
    sshconnection = SSHConnection(host, login, password, port)
    sshconnection.CreateSSHConnection()
    print('SSH connection to %s:%s created.' % (host, port))


    #channel = sshconnection.ExecSSHSocksMakeScript("sudo ./NodeTools/ssh_socks_make.py 10.0.1.3 nickolas")
    hannel = sshconnection.ExecVPNMake("sudo ./NodeTools/vpn_make.py client1.ovpn")
    while True:
        print(">>", end=' ')
        command = input()
        sshconnection.ExecCommand(command)
