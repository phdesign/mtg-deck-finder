import re
from abc import abstractmethod
from ..deck import Deck, DeckEntry
from ..editions import EDITIONS
from .deck_reader_base import DeckReaderBase

LINES_TO_SNIFF = 20


class PatternDeckReader(DeckReaderBase):
    section_pattern = None
    entry_pattern = None

    def __init__(self, readlines, name):
        self.readlines = readlines
        self.deck = Deck(name=name)
        self.current_section = None

    @abstractmethod
    def can_read(self):
        pass

    def read(self):
        for line in self.readlines:
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
    section_pattern = re.compile(r"^(?://)?([A-Za-z]+)$", re.M)
    entry_pattern = re.compile(r"^(\d+) (.+)$", re.M)

    def __init__(self, deck_str, name):
        super().__init__(deck_str, name)
        self.current_section = "main"

    def can_read(self):
        for i, line in enumerate(self.readlines):
            if i > LINES_TO_SNIFF:
                return False
            if self.entry_pattern.search(line):
                return True
        return False


class ApprenticeDeckReader(PatternDeckReader):
    section_pattern = re.compile(r"^\[(.+)\]$", re.M)
    entry_pattern = re.compile(r"^(\d+) (.*?)(\|.*)?$", re.M)

    def can_read(self):
        for i, line in enumerate(self.readlines):
            if i > LINES_TO_SNIFF:
                return False
            if self.section_pattern.search(line):
                return True
        return False

    def _read_line(self, line):
        if self._read_section(line):
            return
        if self.current_section in ["main", "sideboard"]:
            self._read_card(line)


class ArenaDeckReader(PatternDeckReader):
    entry_pattern = re.compile(r"^(\d+) ([^(]+) \(([A-Z0-9_]{3,15})\) (\d+)$", re.M)

    def __init__(self, deck_str, name):
        super().__init__(deck_str, name)
        self.current_section = "main"

    def can_read(self):
        for i, line in enumerate(self.readlines):
            if i > LINES_TO_SNIFF:
                return False
            if self.entry_pattern.search(line):
                return True
        return False

    def _read_card(self, line):
        # A blank line after some entries indicates the sideboard
        if line.strip() == "" and any(self.deck):
            self.current_section = "sideboard"
            return

        match = self.entry_pattern.search(line)
        if match:
            entry = DeckEntry(
                count=int(match.group(1)),
                name=match.group(2),
                edition=self._map_edition(match.group(3)),
                number=int(match.group(4)),
                section=self.current_section,
            )
            self.deck.append(entry)

    def _map_edition(self, code):
        return EDITIONS.get(code, code)
