import collections

DeckEntry = collections.namedtuple('DeckEntry', 'count name')

class Deck(list):
    pass

class ApprenticeDeckReader:
    def __init__(self, deck_str):
        self.deck_str = deck_str

    def can_read(self):
        return True

    def read(self):
        return Deck([
            DeckEntry(count=1, name='Devil')
        ])

class DeckReader:
    def __init__(self, deck_str):
        readers = [ApprenticeDeckReader]

        self.deck_str = deck_str
        self.reader = next(r for r in (r(deck_str) for r in readers) if r.can_read())

    def read(self):
        return self.reader.read()
