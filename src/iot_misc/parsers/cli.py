from argparse import ArgumentParser
from sys import argv

from parsers.toml_config import toml_config

parser = ArgumentParser()

parser.add_argument(
    "-c", "--config", help="Configuration file to use", type=toml_config, required=True
)
parser.add_argument("-n", "--name", help="Session name")
parser.add_argument(
    "-t", "--timestamp", help="Add timestamp to session name", action="store_true"
)

arguments = parser.parse_args()
