from .readers.pattern_deck_reader import ArenaDeckReader, ApprenticeDeckReader, SimpleDeckReader
from .readers.csv_deck_reader import CsvDeckReader


class DeckReader:
    def __init__(self, deckfile, name=None):
        readers = [CsvDeckReader, ArenaDeckReader, ApprenticeDeckReader, SimpleDeckReader]
        self.reader = next((r for r in (r(deckfile, name) for r in readers) if r.can_read()), None)

    def read(self):
        if not self.reader:
            raise ValueError("deck format not supported")
        return self.reader.read()
