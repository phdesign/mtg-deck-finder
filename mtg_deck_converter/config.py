import sys
import argparse

PACKAGE_NAME = "mtg_deck_converter"
VERSION = "0.0.1"


class Config:
    def __getattr__(self, name):
        return getattr(self._args, name)

    def __init__(self):
        self._args = None
        parser = argparse.ArgumentParser(
            description="converts between different magic the gathering deck formats",
            prog=PACKAGE_NAME,
        )
        parser.add_argument(
            "-o", "--outfile", type=argparse.FileType("w"), default=sys.stdout
        )
        parser.add_argument(
            "deck",
            nargs="?",
            type=argparse.FileType("r", errors="ignore"),
            default=sys.stdin,
        )
        self._args = parser.parse_args()

        # Check that we're not waiting on the user to provide stdin input
        if self._args.deck.isatty():
            parser.print_help()
            print("\nerror: no deck file provided", file=sys.stderr)
            sys.exit(2)
