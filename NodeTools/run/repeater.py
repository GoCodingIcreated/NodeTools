import json
from anonymizing_chains.common.logger import configure_logger
from anonymizing_chains.common.argparse import parse_args
from anonymizing_chains.zmq.chain_node import ChainNode


def parse_config(config_path):
    with open(config_path) as config_file:
        data = json.load(config_file)
    return data['network_interface_name'], data['port']


def main():
    args = parse_args()
    configure_logger(args.verbose, args.log)
    iname, port = parse_config(args.config)
    repeater = ChainNode(iname, port)
    repeater.message_loop()
