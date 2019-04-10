import collections

DeckEntry = collections.namedtuple('DeckEntry', ['count', 'name'])

class Deck(list):
    def __init__(self, path=None):
        super().__init__()
        self.path = path
