import argparse
import argparse as ap
import sys


__doc__ = """
    Run entry:
        - prompt
        
"""

from psc_3d.version import VERSION


class ShowVersion(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        print(f"Version: {VERSION}")
        sys.exit(1)


def parser(argv: list = None):
    parser_ = ap.ArgumentParser(description=__doc__)
    parser_.add_argument("-P", "--polymer_type", type=str, required=True, nargs='+',
                         help="Select type of polymer"
                         )
    parser_.add_argument("-S", "--solvent_type", type=str, required=True, nargs='+',
                         help="Select type of solvent"
                         )
    parser_.add_argument("-D", "--data_file", type=str, default='./data.json',
                         help="Data source"
                         )
    parser_.add_argument('--version', action=ShowVersion)
    return parser_.parse_args(argv if argv else sys.argv[1:])

