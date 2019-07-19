import re
from abc import ABC, abstractmethod
from .deck import Deck, DeckEntry

class DeckReaderBase(ABC):
    @abstractmethod
    def can_read(self):
        pass

    @abstractmethod
    def read(self):
        pass

class PatternDeckReader(DeckReaderBase):
    section_pattern = None
    entry_pattern = None

    def __init__(self, deck_str, name):
        self.deck_str = deck_str
        self.deck = Deck(name)
        self.current_section = None

    @abstractmethod
    def can_read(self):
        pass

    def read(self):
        for line in self.deck_str.splitlines():
            self._read_line(line)
        return self.deck

    def _read_line(self, line):
        if self._read_section(line):
            return
        self._read_card(line)

    def _read_section(self, line):
        if self.section_pattern:
            match = self.section_pattern.search(line)
            if match:
                self.current_section = match.group(1).lower()
                return True
        return False

    def _read_card(self, line):
        match = self.entry_pattern.search(line)
        if match:
            entry = DeckEntry(
                count=int(match.group(1)),
                name=match.group(2),
                section=self.current_section)
            self.deck.append(entry)

class SimpleDeckReader(PatternDeckReader):
    section_pattern = re.compile(r"^([A-Za-z]+)$", re.M)
    entry_pattern = re.compile(r"^(\d+) (.+)$", re.M)

    def __init__(self, deck_str, name):
        super().__init__(deck_str, name)
        self.current_section = 'main'

    def can_read(self):
        return self.entry_pattern.search(self.deck_str) is not None

class ApprenticeDeckReader(PatternDeckReader):
    section_pattern = re.compile(r"^\[(.+)\]$", re.M)
    entry_pattern = re.compile(r"^(\d+) (.*?)(\|.*)?$", re.M)

    def can_read(self):
        return self.section_pattern.search(self.deck_str) is not None

    def _read_line(self, line):
        if self._read_section(line):
            return
        if (self.current_section in ['main', 'sideboard']):
            self._read_card(line)

class ArenaDeckReader(PatternDeckReader):
    entry_pattern = re.compile(r"^(\d+) ([^(]+) \(([^)]+)\) (\d+)$", re.M)

    def __init__(self, deck_str, name):
        super().__init__(deck_str, name)
        self.current_section = 'main'

    def can_read(self):
        return self.entry_pattern.search(self.deck_str) is not None

    def _read_card(self, line):
        match = self.entry_pattern.search(line)
        if match:
            entry = DeckEntry(
                count=int(match.group(1)),
                name=match.group(2),
                edition=match.group(3),
                number=int(match.group(4)),
                section=self.current_section)
            self.deck.append(entry)

class DeckReader:
    def __init__(self, deck_str, name=None):
        readers = [ArenaDeckReader, ApprenticeDeckReader, SimpleDeckReader]
        self.reader = next((r for r in (r(deck_str, name) for r in readers) if r.can_read()), None)

    def read(self):
        if not self.reader:
            raise ValueError("deck format not supported")
        return self.reader.read()
