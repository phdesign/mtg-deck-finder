import re
from abc import abstractmethod
from ..deck import Deck, DeckEntry
from .deck_reader_base import DeckReaderBase


class PatternDeckReader(DeckReaderBase):
    section_pattern = None
    entry_pattern = None

    def __init__(self, deckfile, name):
        self.deckfile = deckfile
        self.deck = Deck(name=name)
        self.current_section = None

    @abstractmethod
    def can_read(self):
        pass

    def read(self):
        for line in self.deckfile.readlines():
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
            entry = DeckEntry(count=int(match.group(1)), name=match.group(2), section=self.current_section)
            self.deck.append(entry)


class SimpleDeckReader(PatternDeckReader):
    section_pattern = re.compile(r"^([A-Za-z]+)$", re.M)
    entry_pattern = re.compile(r"^(\d+) (.+)$", re.M)

    def __init__(self, deck_str, name):
        super().__init__(deck_str, name)
        self.current_section = "main"

    def can_read(self):
        result = any(line for line in self.deckfile if self.entry_pattern.search(line))
        self.deckfile.seek(0)
        return result


class ApprenticeDeckReader(PatternDeckReader):
    section_pattern = re.compile(r"^\[(.+)\]$", re.M)
    entry_pattern = re.compile(r"^(\d+) (.*?)(\|.*)?$", re.M)

    def can_read(self):
        result = any(line for line in self.deckfile if self.section_pattern.search(line))
        self.deckfile.seek(0)
        return result

    def _read_line(self, line):
        if self._read_section(line):
            return
        if self.current_section in ["main", "sideboard"]:
            self._read_card(line)


class ArenaDeckReader(PatternDeckReader):
    entry_pattern = re.compile(r"^(\d+) ([^(]+) \(([^)]+)\) (\d+)$", re.M)

    def __init__(self, deck_str, name):
        super().__init__(deck_str, name)
        self.current_section = "main"

    def can_read(self):
        result = any(line for line in self.deckfile if self.entry_pattern.search(line))
        self.deckfile.seek(0)
        return result

    def _read_card(self, line):
        match = self.entry_pattern.search(line)
        if match:
            entry = DeckEntry(
                count=int(match.group(1)),
                name=match.group(2),
                edition=match.group(3),
                number=int(match.group(4)),
                section=self.current_section,
            )
            self.deck.append(entry)
