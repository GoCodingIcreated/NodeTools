import argparse
import json
import zmq


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--config', required=True,
                        help='Configuration file path')
    args = parser.parse_args()

    with open(args.config) as config_file:
        data = json.load(config_file)
    ip, port = data['controller_ip_addr'], data['controller_port']

    context = zmq.Context()
    socket = context.socket(zmq.PAIR)
    socket.connect('tcp://{}:{}'.format(ip, port))

    should_continue = True
    while should_continue:
        s = input()
        if len(s) == 0:
            should_continue = False
        else:
            socket.send_string(s)
