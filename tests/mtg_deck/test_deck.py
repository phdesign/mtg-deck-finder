import json
from mtg_deck.deck import Deck, DeckEntry


class TestDeck:
    def test_normalise_should_group_all_cards_by_name_edition_and_section(self):
        deck = Deck(
            [
                DeckEntry(2, "One", "main", edition="ABC", number=123),
                DeckEntry(3, "Two", "main"),
                DeckEntry(5, "One", "main", edition="ABC", number=123),
                DeckEntry(1, "One", "sideboard"),
                DeckEntry(1, "One", "sideboard"),
            ],
            name="sample",
        )
        normalised_deck = deck.normalise()
        assert json.dumps(normalised_deck.to_json()) == json.dumps(
            {
                "name": "sample",
                "cards": [
                    {"count": 7, "name": "One", "edition": "ABC", "number": 123, "section": "main"},
                    {"count": 2, "name": "One", "edition": None, "number": None, "section": "sideboard"},
                    {"count": 3, "name": "Two", "edition": None, "number": None, "section": "main"},
                ],
            }
        )

    def test_add_should_sum_counts_by_name(self):
        deck = Deck([DeckEntry(count=1, name="Abzan Banner"), DeckEntry(count=3, name="Act of Treason")], name="sample")
        other = Deck(
            [DeckEntry(count=2, name="Abzan Banner"), DeckEntry(count=2, name="Act of Treason")], name="sample2"
        )

        result = deck.add(other)

        assert json.dumps(result.to_json()) == json.dumps(
            {
                "name": "sample",
                "cards": [
                    {"count": 3, "name": "Abzan Banner", "edition": None, "number": None, "section": None},
                    {"count": 5, "name": "Act of Treason", "edition": None, "number": None, "section": None},
                ],
            }
        )

    def test_add_should_not_sum_counts_from_different_editions(self):
        deck = Deck(
            [
                DeckEntry(count=1, name="Abzan Banner", edition="Khans of Tarkir", number=215),
                DeckEntry(count=3, name="Act of Treason", edition="Khans of Tarkir", number=95),
            ],
            name="sample",
        )
        other = Deck(
            [
                DeckEntry(count=2, name="Abzan Banner", edition="Dominaria", number=123),
                DeckEntry(count=2, name="Act of Treason", edition="Khans of Tarkir", number=95),
            ],
            name="sample2",
        )

        result = deck.add(other)

        assert json.dumps(result.to_json()) == json.dumps(
            {
                "name": "sample",
                "cards": [
                    {"count": 2, "name": "Abzan Banner", "edition": "Dominaria", "number": 123, "section": None},
                    {"count": 1, "name": "Abzan Banner", "edition": "Khans of Tarkir", "number": 215, "section": None},
                    {"count": 5, "name": "Act of Treason", "edition": "Khans of Tarkir", "number": 95, "section": None},
                ],
            }
        )

    def test_add_should_not_sum_counts_from_different_sections(self):
        deck = Deck(
            [
                DeckEntry(count=1, name="Abzan Banner", section="main"),
                DeckEntry(count=3, name="Act of Treason", section="main"),
            ],
            name="sample",
        )
        other = Deck(
            [
                DeckEntry(count=2, name="Abzan Banner", section="sideboard"),
                DeckEntry(count=2, name="Act of Treason", section="main"),
            ],
            name="sample2",
        )

        result = deck.add(other)

        assert json.dumps(result.to_json()) == json.dumps(
            {
                "name": "sample",
                "cards": [
                    {"count": 1, "name": "Abzan Banner", "edition": None, "number": None, "section": "main"},
                    {"count": 2, "name": "Abzan Banner", "edition": None, "number": None, "section": "sideboard"},
                    {"count": 5, "name": "Act of Treason", "edition": None, "number": None, "section": "main"},
                ],
            }
        )

    def test_subtract_should_subtract_counts_by_name(self):
        deck = Deck([DeckEntry(count=1, name="Abzan Banner"), DeckEntry(count=3, name="Act of Treason")], name="sample")
        other = Deck(
            [DeckEntry(count=2, name="Abzan Banner"), DeckEntry(count=2, name="Act of Treason")], name="sample2"
        )

        result = deck.subtract(other)

        assert json.dumps(result.to_json()) == json.dumps(
            {
                "name": "sample",
                "cards": [
                    {"count": -1, "name": "Abzan Banner", "edition": None, "number": None, "section": None},
                    {"count": 1, "name": "Act of Treason", "edition": None, "number": None, "section": None},
                ],
            }
        )
