import json
from mtg_deck.deck_reader import DeckReader

APPRENTICE_DECK = """
[metadata]
Name=SaffronOlive - 12 Moon
Format=Modern
[general]
Constructed
[main]
4 Blood Moon
4 Desperate Ritual
4 Ensnaring Bridge
2 Faithless Looting
4 Magus of the Moon
4 Molten Rain
19 Mountain
1 Pyretic Ritual
4 Simian Spirit Guide
1 Stone Rain
1 Gemstone Caverns
2 Chandra, Pyromaster
2 Anger of the Gods
4 Chandra, Torch of Defiance
4 Blood Sun
[sideboard]
2 Pithing Needle
3 Relic of Progenitus
1 Stone Rain
1 Thundermaw Hellkite
4 Trinisphere
2 Anger of the Gods
2 Abrade"""

class TestApprenticeDeckReader:

    def test_should_read_all_cards(self):
        deck_reader = DeckReader(APPRENTICE_DECK, "sample")
        deck = deck_reader.read()
        assert json.dumps(deck.to_json()) == json.dumps({
            'name': "sample",
            'cards': [
                {"count": 4, "name": "Blood Moon", "edition": None, "number": None, "section": "main"},
                {"count": 4, "name": "Desperate Ritual", "edition": None, "number": None, "section": "main"},
                {"count": 4, "name": "Ensnaring Bridge", "edition": None, "number": None, "section": "main"},
                {"count": 2, "name": "Faithless Looting", "edition": None, "number": None, "section": "main"},
                {"count": 4, "name": "Magus of the Moon", "edition": None, "number": None, "section": "main"},
                {"count": 4, "name": "Molten Rain", "edition": None, "number": None, "section": "main"},
                {"count": 19, "name": "Mountain", "edition": None, "number": None, "section": "main"},
                {"count": 1, "name": "Pyretic Ritual", "edition": None, "number": None, "section": "main"},
                {"count": 4, "name": "Simian Spirit Guide", "edition": None, "number": None, "section": "main"},
                {"count": 1, "name": "Stone Rain", "edition": None, "number": None, "section": "main"},
                {"count": 1, "name": "Gemstone Caverns", "edition": None, "number": None, "section": "main"},
                {"count": 2, "name": "Chandra, Pyromaster", "edition": None, "number": None, "section": "main"},
                {"count": 2, "name": "Anger of the Gods", "edition": None, "number": None, "section": "main"},
                {"count": 4, "name": "Chandra, Torch of Defiance", "edition": None, "number": None, "section": "main"},
                {"count": 4, "name": "Blood Sun", "edition": None, "number": None, "section": "main"},
                {"count": 2, "name": "Pithing Needle", "edition": None, "number": None, "section": "sideboard"},
                {"count": 3, "name": "Relic of Progenitus", "edition": None, "number": None, "section": "sideboard"},
                {"count": 1, "name": "Stone Rain", "edition": None, "number": None, "section": "sideboard"},
                {"count": 1, "name": "Thundermaw Hellkite", "edition": None, "number": None, "section": "sideboard"},
                {"count": 4, "name": "Trinisphere", "edition": None, "number": None, "section": "sideboard"},
                {"count": 2, "name": "Anger of the Gods", "edition": None, "number": None, "section": "sideboard"},
                {"count": 2, "name": "Abrade", "edition": None, "number": None, "section": "sideboard"}
            ]
        })

    def test_should_read_main_cards_only_when_sideboard_excluded(self):
        deck_reader = DeckReader(APPRENTICE_DECK, "sample")
        deck = deck_reader.read().without_sideboard()
        assert json.dumps(deck.to_json()) == json.dumps({
            'name': "sample",
            'cards': [
                {"count": 4, "name": "Blood Moon", "edition": None, "number": None, "section": "main"},
                {"count": 4, "name": "Desperate Ritual", "edition": None, "number": None, "section": "main"},
                {"count": 4, "name": "Ensnaring Bridge", "edition": None, "number": None, "section": "main"},
                {"count": 2, "name": "Faithless Looting", "edition": None, "number": None, "section": "main"},
                {"count": 4, "name": "Magus of the Moon", "edition": None, "number": None, "section": "main"},
                {"count": 4, "name": "Molten Rain", "edition": None, "number": None, "section": "main"},
                {"count": 19, "name": "Mountain", "edition": None, "number": None, "section": "main"},
                {"count": 1, "name": "Pyretic Ritual", "edition": None, "number": None, "section": "main"},
                {"count": 4, "name": "Simian Spirit Guide", "edition": None, "number": None, "section": "main"},
                {"count": 1, "name": "Stone Rain", "edition": None, "number": None, "section": "main"},
                {"count": 1, "name": "Gemstone Caverns", "edition": None, "number": None, "section": "main"},
                {"count": 2, "name": "Chandra, Pyromaster", "edition": None, "number": None, "section": "main"},
                {"count": 2, "name": "Anger of the Gods", "edition": None, "number": None, "section": "main"},
                {"count": 4, "name": "Chandra, Torch of Defiance", "edition": None, "number": None, "section": "main"},
                {"count": 4, "name": "Blood Sun", "edition": None, "number": None, "section": "main"}
            ]
        })
