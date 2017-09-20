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





def CreateSSH(node):
    login = nodes[node][0]
    password = nodes[node][1]
    ssh = SSH(node, login, password)
    return ssh

def CreateShell(ssh):
    channel = ssh.client.get_transport().open_session()
    channel.get_pty()
    time.sleep(1)
    shell = ssh.client.invoke_shell()
    shell.setblocking(0)
    time.sleep(1)
    print(shell.recv(10240).decode('utf-8'))
    shell.send("cd /home/nickolas/NodeTools/NodeTools \n")
    return shell

def attach(shell):
    shell.send("tmux attach \n")
    time.sleep(1)

def detach(shell):
    shell.send("\x02\x64")
    time.sleep(1)

def tmux(shell):
    shell.send("tmux \n")
    time.sleep(1)

def startSSHSocks(shell, script, password1, password2):
    shell.send("sudo " + script);
    time.sleep(1)
    shell.send(password1 + '\n')
    time.sleep(10)
    shell.send(password2)
    time.sleep(1)

def closeSSHSocks(shell):
    shell.send("exit")
    time.sleep(1)
    shell.send("\x03")
    time.sleep(1)

def run(node):
    if node[1] == "SSH":
        ssh = CreateSSH(node[0])
        shell = CreateShell(ssh)
        tmux(shell)
        startSSHSocks(shell, "./ssh_socks_make.py " + node[2] + '\n')
        detach(shell)

        time.sleep(30)

        attach(shell)
        closeSSHSocks(shell)
        ssh.closeConnection()



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
    run(chain[0])