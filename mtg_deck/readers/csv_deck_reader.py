from csv import Sniffer, DictReader, Error
from ..deck import Deck, DeckEntry
from .deck_reader_base import DeckReaderBase

class CsvDeckReader(DeckReaderBase):
    def __init__(self, deck_str, name):
        self.lines = deck_str.splitlines()
        self.name = name
        self.deck = None

    def can_read(self):
        try:
            dialect = Sniffer().sniff("\n".join(self.lines[:2]), delimiters=[','])
            print("{!r}".format(dialect))
            return True
        except Error:
            return False

    def read(self):
        csv_reader = DictReader(self.lines, delimiter=',')
        self.deck = Deck((DeckEntry(
            count=int(row["Count"]),
            name=row["Name"],
            edition=row.get("Edition"),
            number=int(row.get("Card Number")),
            section=row.get("Section", "main")
        ) for row in csv_reader), name=self.name)
        return self.deck
