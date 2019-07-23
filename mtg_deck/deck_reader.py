from .readers.pattern_deck_reader import ArenaDeckReader, ApprenticeDeckReader, SimpleDeckReader
from .readers.csv_deck_reader import CsvDeckReader
from .errors import DeckFormatNotSupportedError


class DeckReader:
    def __init__(self, deckfile, name=None):
        readers = [CsvDeckReader, ArenaDeckReader, ApprenticeDeckReader, SimpleDeckReader]
        readlines = deckfile.readlines()
        self.reader = next((r for r in (r(readlines, name) for r in readers) if r.can_read()), None)

    def read(self):
        if not self.reader:
            raise DeckFormatNotSupportedError
        return self.reader.read()
