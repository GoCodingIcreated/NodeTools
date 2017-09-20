#!/usr/bin/python3

import sys
import paramiko

nodes = []
scripts = []

def ParseChainConfig(config):
    commands = []
    with open(config, "r") as file:
        for line in file.readlines():
            try:
                notcomment = line[:-1].split("#")[0]
                command, argv = notcomment.split(";")[0:2]
                ip, type = command.split(' ')[0:2]
                commands.append((ip, type, argv))
            except ValueError:
                pass
    return commands

def ParseGlobalConfig(config):
    commands = []
    with open(config, "r") as file:
        for line in file.readlines():
            command = line[:-1].split("#")[0]
            ip, login, pswd = command.split(" ")[0:3]
            commands.append((ip, login, pswd))
    return commands


class SSH(object):
    def __init__(self, host ,login, password, port=23):
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(hostname=host, username=login,
                       password=password, port=port)
        self.client = client
        #cin, cout, cerr = self.client.exec_command("tmux")
        #print(cout.read())

    def closeConnection(self):
        self.client.close()

    def attach(self):
        cin, cout, cerr = self.client.exec_command("tmux attach")
        print(cout.read())

    def deattach(self):
        cin, cout, cerr = self.client.exec_command("tmux detach")
        print(cout.read())

    def run(self, script):
        cin, cout, cerr = self.client.exec_command(script)
        print(cout.read())




def CreateSSH(node):
    login = nodes[node][0]
    password = nodes[node][1]
    ssh = SSH(node, login, password)
    return ssh


def CreateChain(chain):
    for node in chain:
        ssh = CreateSSH(node[0])
        #ssh.startScript(scripts[node])
        ssh.run("ls -l")

def DestroyChain(chain):
    for node in chain:
        ssh = CreateSSH(node)
        ssh.stopScripts()


if __name__ == "__main__":
    global_config = "config"
    chain_config = "config_chain"
    if len(sys.argv) == 3:
        global_config = sys.argv[1]
        chain_config = sys.argv[2]


    nodes_list = ParseGlobalConfig(global_config)
    nodes = { i[0] : (i[1], i[2]) for i in nodes_list }
    print(nodes)
    chain = ParseChainConfig(chain_config)

    for node in nodes:
        print(node)

    print("")
    for node in chain:
        print(node)
