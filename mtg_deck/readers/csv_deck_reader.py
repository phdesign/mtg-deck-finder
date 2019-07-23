import os
import csv
from ..deck import Deck, DeckEntry
from .deck_reader_base import DeckReaderBase
from ..errors import DeckFormatNotSupportedError


def _try_int(val):
    if val is None:
        return None
    try:
        return int(val)
    except ValueError:
        return None


class CsvDeckReader(DeckReaderBase):
    FIELDNAMES = ["Count", "Name", "Edition", "Card Number", "Section"]

    def __init__(self, readlines, name):
        self.readlines = readlines
        self.name = name
        self.deck = None

    def can_read(self):
        try:
            csv.Sniffer().sniff(os.linesep.join(self.readlines[:3]), delimiters=[","])
            return True
        except csv.Error:
            return False

    def read(self):
        csv_reader = csv.DictReader(self.readlines, delimiter=",")
        try:
            self.deck = Deck(
                (
                    DeckEntry(
                        count=int(row["Count"]),
                        name=row["Name"],
                        edition=row.get("Edition"),
                        number=_try_int(row.get("Card Number")),
                        section=row.get("Section", "main"),
                    )
                    for row in csv_reader
                ),
                name=self.name,
            )
            return self.deck
        except (KeyError, ValueError):
            raise DeckFormatNotSupportedError
