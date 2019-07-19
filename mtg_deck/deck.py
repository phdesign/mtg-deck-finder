class DeckEntry:
    def __init__(self, count, name, section=None, edition=None, number=None):
        self.count = count
        self.name = name
        self.edition = edition
        self.number = number
        self.section = section

class Deck(list):
    def __init__(self, name=None):
        super().__init__()
        self.name = name

    def without_sideboard(self):
        return [e for e in self if e.section.lower() != 'sideboard']
