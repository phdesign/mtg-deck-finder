from ..deck import Deck, DeckEntry
from .deck_reader_base import DeckReaderBase

class CsvDeckReader(DeckReaderBase):
    def __init__(self, deck_str, name):
        self.deck_str = deck_str
        self.deck = Deck(name)

    def can_read(self):
        pass

    def read(self):
        pass
