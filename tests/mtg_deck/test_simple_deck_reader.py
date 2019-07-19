import json
from mtg_deck.deck_reader import DeckReader

MTGTOP8_DECK = """
4 Broken Ambitions
4 Reflecting Pool
4 Vivid Grove
4 Cryptic Command
4 Fulminator Mage
4 Sunken Ruins
4 Vivid Creek
4 Mulldrifter
3 Firespout
3 Cloudthresher
3 Forest
3 Fire-Lit Thicket
3 Makeshift Mannequin
3 Mind Spring
3 Island
2 Shriekmaw
2 Austere Command
2 Nameless Inversion
1 Wooded Bastion
Sideboard
1 Firespout
1 Shriekmaw
4 Kitchen Finks
2 Primal Command
2 Mind Shatter
2 Negate
2 Sower of Temptation
1 Final Revels"""

class TestSimpleDeckReader:
    
    def test_should_read_all_cards(self):
        deck_reader = DeckReader(MTGTOP8_DECK, "sample")
        deck = deck_reader.read()
        assert json.dumps(deck.to_json()) == json.dumps({
            'name': "sample",
            'cards': [
                {"count": 4, "name": "Broken Ambitions", "edition": None, "number": None, "section": "main"},
                {"count": 4, "name": "Reflecting Pool", "edition": None, "number": None, "section": "main"},
                {"count": 4, "name": "Vivid Grove", "edition": None, "number": None, "section": "main"},
                {"count": 4, "name": "Cryptic Command", "edition": None, "number": None, "section": "main"},
                {"count": 4, "name": "Fulminator Mage", "edition": None, "number": None, "section": "main"},
                {"count": 4, "name": "Sunken Ruins", "edition": None, "number": None, "section": "main"},
                {"count": 4, "name": "Vivid Creek", "edition": None, "number": None, "section": "main"},
                {"count": 4, "name": "Mulldrifter", "edition": None, "number": None, "section": "main"},
                {"count": 3, "name": "Firespout", "edition": None, "number": None, "section": "main"},
                {"count": 3, "name": "Cloudthresher", "edition": None, "number": None, "section": "main"},
                {"count": 3, "name": "Forest", "edition": None, "number": None, "section": "main"},
                {"count": 3, "name": "Fire-Lit Thicket", "edition": None, "number": None, "section": "main"},
                {"count": 3, "name": "Makeshift Mannequin", "edition": None, "number": None, "section": "main"},
                {"count": 3, "name": "Mind Spring", "edition": None, "number": None, "section": "main"},
                {"count": 3, "name": "Island", "edition": None, "number": None, "section": "main"},
                {"count": 2, "name": "Shriekmaw", "edition": None, "number": None, "section": "main"},
                {"count": 2, "name": "Austere Command", "edition": None, "number": None, "section": "main"},
                {"count": 2, "name": "Nameless Inversion", "edition": None, "number": None, "section": "main"},
                {"count": 1, "name": "Wooded Bastion", "edition": None, "number": None, "section": "main"},
                {"count": 1, "name": "Firespout", "edition": None, "number": None, "section": "sideboard"},
                {"count": 1, "name": "Shriekmaw", "edition": None, "number": None, "section": "sideboard"},
                {"count": 4, "name": "Kitchen Finks", "edition": None, "number": None, "section": "sideboard"},
                {"count": 2, "name": "Primal Command", "edition": None, "number": None, "section": "sideboard"},
                {"count": 2, "name": "Mind Shatter", "edition": None, "number": None, "section": "sideboard"},
                {"count": 2, "name": "Negate", "edition": None, "number": None, "section": "sideboard"},
                {"count": 2, "name": "Sower of Temptation", "edition": None, "number": None, "section": "sideboard"},
                {"count": 1, "name": "Final Revels", "edition": None, "number": None, "section": "sideboard"}
            ]
        })

    def test_should_read_main_cards_only_when_sideboard_excluded(self):
        deck_reader = DeckReader(MTGTOP8_DECK, "sample")
        deck = deck_reader.read().without_sideboard()
        assert json.dumps(deck.to_json()) == json.dumps({
            'name': "sample",
            'cards': [
                {"count": 4, "name": "Broken Ambitions", "edition": None, "number": None, "section": "main"},
                {"count": 4, "name": "Reflecting Pool", "edition": None, "number": None, "section": "main"},
                {"count": 4, "name": "Vivid Grove", "edition": None, "number": None, "section": "main"},
                {"count": 4, "name": "Cryptic Command", "edition": None, "number": None, "section": "main"},
                {"count": 4, "name": "Fulminator Mage", "edition": None, "number": None, "section": "main"},
                {"count": 4, "name": "Sunken Ruins", "edition": None, "number": None, "section": "main"},
                {"count": 4, "name": "Vivid Creek", "edition": None, "number": None, "section": "main"},
                {"count": 4, "name": "Mulldrifter", "edition": None, "number": None, "section": "main"},
                {"count": 3, "name": "Firespout", "edition": None, "number": None, "section": "main"},
                {"count": 3, "name": "Cloudthresher", "edition": None, "number": None, "section": "main"},
                {"count": 3, "name": "Forest", "edition": None, "number": None, "section": "main"},
                {"count": 3, "name": "Fire-Lit Thicket", "edition": None, "number": None, "section": "main"},
                {"count": 3, "name": "Makeshift Mannequin", "edition": None, "number": None, "section": "main"},
                {"count": 3, "name": "Mind Spring", "edition": None, "number": None, "section": "main"},
                {"count": 3, "name": "Island", "edition": None, "number": None, "section": "main"},
                {"count": 2, "name": "Shriekmaw", "edition": None, "number": None, "section": "main"},
                {"count": 2, "name": "Austere Command", "edition": None, "number": None, "section": "main"},
                {"count": 2, "name": "Nameless Inversion", "edition": None, "number": None, "section": "main"},
                {"count": 1, "name": "Wooded Bastion", "edition": None, "number": None, "section": "main"}
            ]
        })