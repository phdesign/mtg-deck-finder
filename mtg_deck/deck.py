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
    def __init__(self, name=None):
        super().__init__()
        self.name = name

    
    def to_json(self):
        '''
        Returns a serialised object (not a JSON string!) ready to be passed to json.dumps
        '''
        return [e.to_json() for e in self]

    def without_sideboard(self):
        return [e for e in self if e.section != 'sideboard']
