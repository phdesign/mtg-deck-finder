import sys
import argparse

PACKAGE_NAME = "mtg_deck_finder"
VERSION = "0.0.1"


class Config:
    FORMAT_TABLE = "table"
    FORMAT_JSON = "json"
    FORMAT_PERCENT = "percent"

    def __getattr__(self, name):
        return getattr(self._args, name)

    def __init__(self):
        self._args = None
        parser = argparse.ArgumentParser(
            description="attempts to find magic the gathering decks that can be built from an inventory",
            prog=PACKAGE_NAME,
        )
        parser.add_argument(
            "-o",
            "--output-format",
            default=self.FORMAT_TABLE,
            choices=[self.FORMAT_TABLE, self.FORMAT_JSON, self.FORMAT_PERCENT],
            help='output format, "table", "json" or "percent"',
        )
        parser.add_argument(
            "-i",
            "--inventory",
            required=True,
            type=argparse.FileType("r"),
            help="inventory file of mtg cards available",
        )
        parser.add_argument(
            "deck",
            nargs="?",
            type=argparse.FileType("r", errors="ignore"),
            default=sys.stdin,
            help="deck to compare against inventory",
        )
        self._args = parser.parse_args()

        # Check that we're not waiting on the user to provide stdin input
        if self._args.deck.isatty():
            parser.print_help()
            print("\nerror: no deck file provided", file=sys.stderr)
            sys.exit(2)
