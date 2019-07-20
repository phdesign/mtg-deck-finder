from itertools import groupby
from functools import reduce
import operator


def group(deck, name, countfunc):
    keyfunc = lambda x: (x.name, x.edition is None, x.edition, x.number is None, x.number, x.section is None, x.section)
    cards = sorted(deck, key=keyfunc)
    return Deck(
        (
            DeckEntry(count=countfunc(group), name=key[0], edition=key[2], number=key[4], section=key[6])
            for key, group in groupby(cards, keyfunc)
        ),
        name=name,
    )


class DeckEntry:
    def __init__(self, count, name, section=None, edition=None, number=None):
        self.count = count
        self.name = name
        self.edition = edition
        self.number = number
        self.section = section

    def to_json(self):
        """Returns a serialised object (not a JSON string!) ready to be passed to json.dumps."""
        return self.__dict__


class Deck(list):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = kwargs.get("name")

    def to_json(self):
        """Returns a serialised object (not a JSON string!) ready to be passed to json.dumps."""
        return {"name": self.name, "cards": [e.to_json() for e in self]}

    def without_sideboard(self):
        """Returns a copy of the current deck without the sideboard cards."""
        return Deck((e for e in self if e.section != "sideboard"), name=self.name)

    def exclude_metadata(self):
        return Deck((DeckEntry(count=e.count, name=e.name) for e in self), name=self.name)

    def normalise(self):
        """Returns a copy of the current deck with cards grouped by name, summing the count."""
        return group(self, self.name, lambda g: sum(e.count for e in g))

    def add(self, other):
        return group(self + other, self.name, lambda g: sum(e.count for e in g))

    def subtract(self, other):
        return group(self + other, self.name, lambda g: reduce(operator.__sub__, (e.count for e in g)))
