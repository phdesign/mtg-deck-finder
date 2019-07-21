from itertools import groupby
from functools import total_ordering


def _keyfunc(entry):
    return (
        entry.name,
        entry.edition is None,
        entry.edition,
        entry.number is None,
        entry.number,
        entry.section is None,
        entry.section,
    )


def _group(deck, name, countfunc):
    cards = sorted(deck)
    return Deck(
        (
            x
            for x in (
                DeckEntry(count=countfunc(key, group), name=key[0], edition=key[2], number=key[4], section=key[6])
                for key, group in groupby(cards, _keyfunc)
            )
            if x.count > 0
        ),
        name=name,
    )


@total_ordering
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

    def __lt__(self, other):
        return _keyfunc(self) < _keyfunc(other)

    def __eq__(self, other):
        return _keyfunc(self) == _keyfunc(other)


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
        return _group(self, self.name, lambda _, g: sum(e.count for e in g))

    def add(self, other):
        return _group(self + other, self.name, lambda _, g: sum(e.count for e in g))

    def subtract(self, other):
        othergroup = {k: list(v) for k, v in groupby(other, _keyfunc)}
        subfunc = (
            lambda k, g: sum(e.count for e in g) - sum(e.count for e in othergroup[k])
            if k in othergroup
            else sum(e.count for e in g)
        )
        return _group(self, self.name, subfunc)
