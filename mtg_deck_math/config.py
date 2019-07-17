import sys
import argparse

PACKAGE_NAME = 'mtg_deck_math'
VERSION = '0.0.1'

class Config:
    def __getattr__(self, name):
        return getattr(self._args, name)

    def __init__(self):
        self._args = None
        parser = argparse.ArgumentParser(
            description="some deck arithmetic",
            prog=PACKAGE_NAME)
        parser.add_argument('-a', '--add', help='perform addition')
        parser.add_argument('-s', '--subtract', help='perform subtraction')
        parser.add_argument('first', nargs='?', type=argparse.FileType('r', errors='ignore'),
                            help="first deck")
        parser.add_argument('second', nargs='?', type=argparse.FileType('r', errors='ignore'),
                            help="first deck")
        self._args = parser.parse_args()

        # Check that we're not waiting on the user to provide stdin input
        if not self._args.first or not self._args.second:
            parser.print_help()
            sys.exit(2)
