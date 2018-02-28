#!/usr/bin/python3

import sys
import paramiko
import time
import json

nodes = {}


global_config = "./configure/config.json"
chain_config = "./configure/config_chain.json"

CONFIG_SSH = "./configure/ssh_socks_make_config.json"
CONFIG_SOCKS = "./configure/socks_make_config.json"
LOGFILE = 'log.out'
SCRIPT_START_SSH = "./node/ssh_socks_make.py %s " % CONFIG_SSH
SCRIPT_START_SOCKS = "./node/socks_make.py %s " % CONFIG_SOCKS
SCRIPT_START_VPN = "./node/vpn_make.py "
SCRIPT_START_VPN_ROUTING = "./node/vpn_routing.py "
DIR = "~/NodeTools/NodeTools/"

def ParseChainConfig(config):
    with open(config, "r") as file:
        data = json.load(file)
    return data["chain"]

def ParseGlobalConfig(config):
    global CONFIG_SOCKS, CONFIG_SSH, LOGFILE, \
        SCRIPT_START_VPN, SCRIPT_START_SOCKS,\
        SCRIPT_START_SSH, SCRIPT_START_VPN_ROUTING,\
        DIR
    with open(config, "r") as file:
        data = json.load(file)

    LOGFILE = data["LOGFILE"]
    SCRIPT_START_SSH = data["SCRIPT_START_SSH"]
    SCRIPT_START_SOCKS = data["SCRIPT_START_SOCKS"]
    SCRIPT_START_VPN = data["SCRIPT_START_VPN"]
    SCRIPT_START_VPN_ROUTING = data["SCRIPT_START_VPN_ROUTING"]
    DIR = data["DIR"]
    return data["pull"]


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
    with open(LOGFILE, "a") as file:
        file.write(shell.recv(10240).decode('utf-8'))
    shell.send("cd " + DIR + "\n")
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

def tmuxExit(shell):
    shell.send("exit\n")
    time.sleep(1)

def startSSHSocks(shell, script, password1, password2):
    shell.send("sudo " + script)
    time.sleep(1)
    shell.send(password1 + '\n')
    time.sleep(10)
    shell.send(password2 + '\n')
    time.sleep(1)

def closeSSHSocks(shell):
    shell.send("exit\n")
    time.sleep(1)
    shell.send("\x03")
    time.sleep(1)

def startSocks(shell, script, password):
    shell.send("sudo " + script)
    time.sleep(1)
    shell.send(password + '\n')
    time.sleep(3)

def closeSocks(shell):
    shell.send("\x03")
    time.sleep(1)

def startVPN(shell, script, password):
    shell.send("sudo " + script)
    time.sleep(1)
    shell.send(password + '\n')
    time.sleep(10)


def closeVPN(shell):
    shell.send("\x03")
    time.sleep(1)

def addVPNroutingClient(shell, password):
    shell.send("sudo " + SCRIPT_START_VPN_ROUTING  + "client\n")
    time.sleep(1)
    shell.send(password + '\n')
    time.sleep(1)

def addVPNroutingServer(shell, password):
    shell.send("sudo " + SCRIPT_START_VPN_ROUTING + "server\n")
    time.sleep(1)
    shell.send(password + '\n')
    time.sleep(1)

def run(node):
    if node[1] == "SSH":
        ssh = CreateSSH(node[0])
        shell = CreateShell(ssh)
        tmux(shell)
        target_ip = node[2]
        target_password = nodes[target_ip][1]

        startSSHSocks(shell, SCRIPT_START_SSH + node[3] + '\n', nodes[node[0]][1], target_password)
        detach(shell)

        output = shell.recv(100000).decode('utf-8')
        with open(LOGFILE, "a") as file:
            file.write(output)

        ssh.closeConnection()

    elif node[1] == "SOCKS":
        ssh = CreateSSH(node[0])
        shell = CreateShell(ssh)
        tmux(shell)

        startSocks(shell, SCRIPT_START_SOCKS + node[3] + '\n', nodes[node[0]][1])
        detach(shell)

        output = shell.recv(100000).decode('utf-8')
        with open(LOGFILE, "a") as file:
            file.write(output)
        ssh.closeConnection()

    elif node[1] == "VPN":
        ssh = CreateSSH(node[0])
        shell = CreateShell(ssh)
        tmux(shell)

        startVPN(shell, SCRIPT_START_VPN + node[3] + '\n', nodes[node[0]][1])
        detach(shell)
        addVPNroutingClient(shell, nodes[node[0]][1])

        output = shell.recv(100000).decode('utf-8')
        with open(LOGFILE, "a") as file:
            file.write(output)
        ssh.closeConnection()

        ssh = CreateSSH(node[2])
        shell = CreateShell(ssh)
        addVPNroutingServer(shell, nodes[node[2]][1])
        ssh.closeConnection()
    else:
        return


def destroy(node):
    print("Destroy")
    if node[1] == "SSH":
        ssh = CreateSSH(node[0])
        shell = CreateShell(ssh)

        attach(shell)
        closeSSHSocks(shell)
        tmuxExit(shell)
        output = shell.recv(100000).decode('utf-8')
        with open(LOGFILE, "a") as file:
            file.write(output)
        ssh.closeConnection()

    elif node[1] == "SOCKS":
        ssh = CreateSSH(node[0])
        shell = CreateShell(ssh)

        attach(shell)
        closeSocks(shell)
        tmuxExit(shell)
        output = shell.recv(100000).decode('utf-8')
        with open(LOGFILE, "a") as file:
            file.write(output)
        ssh.closeConnection()

    elif node[1] == "VPN":
        ssh = CreateSSH(node[0])
        shell = CreateShell(ssh)
        attach(shell)
        closeVPN(shell)
        tmuxExit(shell)
        output = shell.recv(100000).decode('utf-8')
        with open(LOGFILE, "a") as file:
            file.write(output)
    else:
        return

def CreateChain(chain):
    for node in chain:
        run(node)

def DestroyChain(chain):
    for node in chain:
        destroy(node)


def SetUp(global_con = global_config):
    global nodes
    nodes_list = ParseGlobalConfig(global_config)
    nodes = { i[0] : (i[1], i[2]) for i in nodes_list }
    print(nodes)


if __name__ == "__main__":
    if len(sys.argv) == 3:
        global_config = sys.argv[1]
        chain_config = sys.argv[2]

    SetUp(global_config)
    chain = ParseChainConfig(chain_config)

    for node in nodes:
        print(node)


    CreateChain(chain)

    time.sleep(180)
    DestroyChain(chain)
