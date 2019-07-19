from itertools import groupby

class DeckEntry:
    def __init__(self, count, name, section=None, edition=None, number=None):
        self.count = count
        self.name = name
        self.edition = edition
        self.number = number
        self.section = section

    def to_json(self):
        '''
        Returns a serialised object (not a JSON string!) ready to be passed to json.dumps
        '''
        return self.__dict__


class Deck(list):
    def __init__(self, name=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = name

    def to_json(self):
        '''
        Returns a serialised object (not a JSON string!) ready to be passed to json.dumps.
        '''
        return { 'name': self.name, 'cards': [e.to_json() for e in self] }

    def without_sideboard(self):
        '''
        Returns a copy of the current deck without the sideboard cards.
        '''
        return Deck(self.name, (e for e in self if e.section != 'sideboard'))

    def normalise(self):
        '''
        Returns a copy of the current deck with cards grouped by name, summing the count.
        '''
        keyfunc = lambda x: (x.name, x.section)
        cards = sorted(self, key=keyfunc)
        return Deck(self.name, (DeckEntry(count=sum(e.count for e in group), name=key[0], section=key[1]) for key, group in groupby(cards, keyfunc)))
