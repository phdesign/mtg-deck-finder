import collections

class DeckEntry:
    def __init__(self, count, name, edition=None, number=None):
        self.count = count
        self.name = name
        self.edition = edition
        self.number = number

class Deck(list):
    def __init__(self, path=None):
        super().__init__()
        self.path = path
