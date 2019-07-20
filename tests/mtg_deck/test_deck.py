import json
from mtg_deck.deck import Deck, DeckEntry

class TestDeck:
    
    def test_normalise_should_read_group_all_cards_in_section(self):
        deck = Deck([
            DeckEntry(2, "One", "main", edition="ABC",number=123),
            DeckEntry(3, "Two", "main"),
            DeckEntry(5, "One", "main", edition="ABC",number=123),
            DeckEntry(1, "One", "sideboard"),
            DeckEntry(1, "One", "sideboard")
        ], name="sample")
        normalised_deck = deck.normalise()
        assert json.dumps(normalised_deck.to_json()) == json.dumps({
            'name': "sample",
            'cards': [
                {"count": 7, "name": "One", "edition": None, "number": None, "section": "main"},
                {"count": 2, "name": "One", "edition": None, "number": None, "section": "sideboard"},
                {"count": 3, "name": "Two", "edition": None, "number": None, "section": "main"}
            ]
        })
