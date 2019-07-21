import sys
import argparse
from pkg_resources import get_distribution

__pkg_name__ = __name__.partition(".")[0].replace('_', '-')
__version__ = get_distribution('mtg-deck').version


class Config:
    ADD = "add"
    CAT = "cat"
    NORMALISE = "normalise"
    NO_SIDEBOARD = "no-sideboard"
    STRIP_META = "strip-meta"
    SUBTRACT = "subtract"

    JSON = "json"
    CSV = "csv"
    COUNT = "count"

    def __getattr__(self, name):
        return getattr(self._args, name)

    def __init__(self):
        self._args = None
        parser = argparse.ArgumentParser(description="performs magic deck operations", prog=__pkg_name__)

        parser.add_argument(
            "operation",
            choices=[self.ADD, self.CAT, self.NORMALISE, self.NO_SIDEBOARD, self.STRIP_META, self.SUBTRACT],
            default=None,
            help="operation to perform",
        )
        parser.add_argument(
            "-f",
            "--output-format",
            default=self.CSV,
            choices=[self.CSV, self.JSON, self.COUNT],
            help='output format',
        )
        parser.add_argument("-o", "--outfile", type=argparse.FileType("w"), default=sys.stdout)
        parser.add_argument("deck", nargs="?", type=argparse.FileType("r", errors="ignore"), default=sys.stdin)
        parser.add_argument("other", nargs="?", type=argparse.FileType("r", errors="ignore"))
        parser.add_argument('--version', action='version', version='%(prog)s ' + __version__)
        self._args = parser.parse_args()

        # Check that we're not waiting on the user to provide stdin input
        if self._args.deck.isatty():
            parser.print_help()
            sys.exit(2)
