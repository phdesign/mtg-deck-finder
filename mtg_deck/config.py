import sys
import argparse
from pkg_resources import get_distribution

__pkg_name__ = __name__.partition(".")[0].replace("_", "-")
__version__ = get_distribution("mtg-deck").version


class Config:
    ADD = "add"
    NORMALISE = "normalise"
    NO_SIDEBOARD = "no-sideboard"
    STRIP_META = "strip-meta"
    SUBTRACT = "subtract"
    SORT = "sort"

    JSON = "json"
    CSV = "csv"
    COUNT = "count"

    def __getattr__(self, name):
        return getattr(self._args, name)

    def __init__(self):
        self._args = None
        parser = argparse.ArgumentParser(
            description="performs magic deck operations",
            epilog="operations may be combined, order is preserved",
            prog=__pkg_name__,
        )

        parser.add_argument(
            "--add",
            dest="operations",
            action="append_const",
            const=self.ADD,
            help="add decks together, combining the counts",
        )
        parser.add_argument(
            "--normalise",
            dest="operations",
            action="append_const",
            const=self.NORMALISE,
            help="normalise a deck(s), combining any duplicate entries and summing the counts",
        )
        parser.add_argument(
            "--no-sideboard",
            dest="operations",
            action="append_const",
            const=self.NO_SIDEBOARD,
            help="remove sideboard cards from the deck(s)",
        )
        parser.add_argument(
            "--strip-meta",
            dest="operations",
            action="append_const",
            const=self.STRIP_META,
            help="remove metadata from the deck(s), retaining only count and name",
        )
        parser.add_argument(
            "--subtract",
            dest="operations",
            action="append_const",
            const=self.SUBTRACT,
            help="subtract the decks, removing the cards in the second deck from the first",
        )
        parser.add_argument(
            "--sort", dest="operations", action="append_const", const=self.SORT, help="sort the deck(s)"
        )
        parser.add_argument(
            "-f", "--output-format", default=self.CSV, choices=[self.CSV, self.JSON, self.COUNT], help="output format"
        )
        parser.add_argument("-o", "--outfile", type=argparse.FileType("w"), default=sys.stdout)
        parser.add_argument("deck", type=argparse.FileType("r", errors="ignore"), default=sys.stdin)
        parser.add_argument(
            "other",
            nargs="?",
            type=argparse.FileType("r", errors="ignore"),
            help="other deck for operations such as add, subtract",
        )
        parser.add_argument("--version", action="version", version="%(prog)s " + __version__)
        self._args = parser.parse_args()

        # Check that we're not waiting on the user to provide stdin input
        if self._args.deck.isatty():
            parser.print_help()
            sys.exit(2)
