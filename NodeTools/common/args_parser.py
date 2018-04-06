import argparse


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--config', required=True,
                        help='Configuration file path')
    parser.add_argument('-l', '--log', default=None,
                        help='Log file path')
    parser.add_argument('-v', '--verbose', action='count', default=0,
                        help='Verbosity level (-v, -vv, -vvv)')
    return parser.parse_args()
