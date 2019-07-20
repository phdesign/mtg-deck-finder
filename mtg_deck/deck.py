from itertools import groupby
from functools import reduce
import operator


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

    def normalise(self):
        """Returns a copy of the current deck with cards grouped by name, summing the count."""
        keyfunc = lambda x: (x.name, x.section)
        cards = sorted(self, key=keyfunc)
        return Deck(
            (
                DeckEntry(
                    count=sum(e.count for e in group), name=key[0], section=key[1]
                )
                for key, group in groupby(cards, keyfunc)
            ),
            name=self.name,
        )

    def add(self, other):
        keyfunc = lambda x: (x.name, x.edition, x.number, x.section)
        cards = sorted(self + other, key=keyfunc)
        return Deck(
            (
                DeckEntry(
                    count=sum(e.count for e in group),
                    name=key[0],
                    edition=key[1],
                    number=key[2],
                    section=key[3],
                )
                for key, group in groupby(cards, keyfunc)
            ),
            name=self.name,
        )

    def subtract(self, other):
        keyfunc = lambda x: (x.name, x.edition, x.number, x.section)
        cards = sorted(self + other, key=keyfunc)
        return Deck(
            (
                DeckEntry(
                    count=reduce(operator.__sub__, (e.count for e in group)),
                    name=key[0],
                    edition=key[1],
                    number=key[2],
                    section=key[3],
                )
                for key, group in groupby(cards, keyfunc)
            ),
            name=self.name,
        )
