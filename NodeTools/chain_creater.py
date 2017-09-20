#!/usr/bin/python3

import sys
import paramiko
import time

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
    def __init__(self, host ,login, password, port=22):
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(hostname=host, username=login,
                       password=password, port=port)
        self.client = client

    def closeConnection(self):
        print("Close")
        self.client.close()

    def startTmux(self):
        print("Start")
        cin, cout, cerr = self.client.exec_command("tmux")
        print(cout.read().decode('utf-8'))
        print(cerr.read().decode('utf-8'))

    def attach(self):
        print("Attach")
        cin, cout, cerr = self.client.exec_command("tmux attach")
        print(cout.read().decode('utf-8'))
        print(cerr.read().decode('utf-8'))

    def deattach(self):
        print("Deattach")
        cin, cout, cerr = self.client.exec_command("tmux detach")
        print(cout.read().decode('utf-8'))
        print(cerr.read().decode('utf-8'))

    def run(self, script):
        print("Run")
        cin, cout, cerr = self.client.exec_command(script)
        print(cout.read().decode('utf-8'))
        print(cerr.read().decode('utf-8'))




def CreateSSH(node):
    login = nodes[node][0]
    password = nodes[node][1]
    ssh = SSH(node, login, password)
    return ssh

def test(node):
    ssh = CreateSSH(node[0])
    ssh.startTmux()
    ssh.run("/home/nickolas/NodeTools/a.out &")
    ssh.deattach()
    ssh.closeConnection()

    ssh = CreateSSH(node[0])
    ssh.attach()
    ssh.run("exit")
    ssh.deattach()
    ssh.closeConnection()


def test2(node):
    ssh = CreateSSH(node[0])
    channel = ssh.client.get_transport().open_session()
    pty = channel.get_pty()
    time.sleep(1)
    shell = ssh.client.invoke_shell()
    shell.setblocking(0)


    time.sleep(1)
    print(shell.recv(10240).decode('utf-8'))
    shell.send("cd /home/nickolas/NodeTools/NodeTools \n")
    time.sleep(1)
    shell.send("tmux \n")
    time.sleep(1)
    shell.send("sudo ./ssh_socks_make.py 10.0.1.3 nickolas >temp \n")
    time.sleep(1)
    shell.send("455722\n")
    time.sleep(10)
    shell.send("455722\n")
    shell.send("\x02\x64")
    time.sleep(1)
    shell.send("head out\n")
    time.sleep(1)
    time.sleep(3)
    shell.send("tmux attach\n")
    time.sleep(30)
    shell.send("exit\n")
    time.sleep(1)
    shell.send("\x03")
    time.sleep(1)
    shell.send("head out\n")
    time.sleep(1)

    with open("temp", "w") as file:
        print(shell.recv(10240).decode('utf-8'), file=file)


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

    #CreateChain(chain)
    test2(chain[0])