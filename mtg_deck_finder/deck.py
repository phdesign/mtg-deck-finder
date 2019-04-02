import collections
import re

DeckEntry = collections.namedtuple('DeckEntry', ['count', 'name'])

class Deck(list):
    def __init__(self, path=None):
        super().__init__()
        self.path = path

class TextDeckReader:
    entry_pattern = re.compile(r"^(\d+) (.*)$", re.M)

    def __init__(self, deck_str, path):
        self.deck_str = deck_str
        self.deck = Deck(path)

    def can_read(self):
        return self.entry_pattern.search(self.deck_str) is not None

    def read(self):
        for line in self.deck_str.splitlines():
            self._read_line(line)
        return self.deck

    def _read_line(self, line):
        match = re.search(r"^(\d+) (.*)$", line)
        self.deck.append(DeckEntry(count=int(match.group(1)), name=match.group(2)))

class ApprenticeDeckReader:
    section_pattern = re.compile(r"^\[(.*)\]$", re.M)
    entry_pattern = re.compile(r"^(\d+) (.*?)(\|.*)?$", re.M)

    def __init__(self, deck_str, path):
        self.deck_str = deck_str
        self.current_section = None
        self.deck = Deck(path)

    def can_read(self):
        return self.section_pattern.search(self.deck_str) is not None

    def read(self):
        for line in self.deck_str.splitlines():
            self._read_line(line)
        return self.deck

    def _read_line(self, line):
        match = self.section_pattern.search(line)
        if match:
            self.current_section = match.group(1).lower()
            return

        if self.current_section == 'main':
            match = self.entry_pattern.search(line)
            self.deck.append(DeckEntry(count=int(match.group(1)), name=match.group(2)))

class DeckReader:
    def __init__(self, deck_str, path=None):
        readers = [ApprenticeDeckReader, TextDeckReader]
        self.reader = next((r for r in (r(deck_str, path) for r in readers) if r.can_read()), None)

    def read(self):
        if not self.reader:
            raise ValueError("deck format not supported")
        return self.reader.read()
