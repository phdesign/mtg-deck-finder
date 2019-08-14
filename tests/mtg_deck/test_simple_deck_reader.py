import json
from io import StringIO
from mtg_deck.deck_reader import DeckReader
from .fixtures import MTGTOP8_DECK, WIZARDS_DECK_WITH_COMMA


class TestSimpleDeckReader:
    def test_should_read_all_cards(self):
        deck = DeckReader(StringIO(MTGTOP8_DECK), "sample").read()
        assert json.dumps(deck.to_json()) == json.dumps(
            {
                "name": "sample",
                "cards": [
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
                    {
                        "count": 2,
                        "name": "Sower of Temptation",
                        "edition": None,
                        "number": None,
                        "section": "sideboard",
                    },
                    {"count": 1, "name": "Final Revels", "edition": None, "number": None, "section": "sideboard"},
                ],
            }
        )

    def test_should_read_main_cards_only_when_sideboard_excluded(self):
        deck = DeckReader(StringIO(MTGTOP8_DECK), "sample").read().without_sideboard()
        assert json.dumps(deck.to_json()) == json.dumps(
            {
                "name": "sample",
                "cards": [
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
                ],
            }
        )

    def test_should_read_cards_given_comma_in_title(self):
        deck = DeckReader(StringIO(WIZARDS_DECK_WITH_COMMA), "sample").read()
        assert json.dumps(deck.to_json()) == json.dumps(
            {
                "name": "sample",
                "cards": [
                    {
                        "count": 4,
                        "name": "Nissa, Who Shakes the World",
                        "edition": None,
                        "number": None,
                        "section": "main",
                    },
                    {
                        "count": 1,
                        "name": "Teferi, Hero of Dominaria",
                        "edition": None,
                        "number": None,
                        "section": "main",
                    },
                    {"count": 4, "name": "Teferi, Time Raveler", "edition": None, "number": None, "section": "main"},
                    {"count": 2, "name": "Frilled Mystic", "edition": None, "number": None, "section": "main"},
                    {"count": 4, "name": "Hydroid Krasis", "edition": None, "number": None, "section": "main"},
                    {"count": 4, "name": "Llanowar Elves", "edition": None, "number": None, "section": "main"},
                    {"count": 4, "name": "Paradise Druid", "edition": None, "number": None, "section": "main"},
                    {"count": 2, "name": "Drawn from Dreams", "edition": None, "number": None, "section": "main"},
                    {"count": 2, "name": "Entrancing Melody", "edition": None, "number": None, "section": "main"},
                    {"count": 3, "name": "Mass Manipulation", "edition": None, "number": None, "section": "main"},
                    {"count": 4, "name": "Growth Spiral", "edition": None, "number": None, "section": "main"},
                    {"count": 2, "name": "Prison Realm", "edition": None, "number": None, "section": "main"},
                    {"count": 4, "name": "Breeding Pool", "edition": None, "number": None, "section": "main"},
                    {"count": 3, "name": "Forest", "edition": None, "number": None, "section": "main"},
                    {"count": 3, "name": "Glacial Fortress", "edition": None, "number": None, "section": "main"},
                    {"count": 4, "name": "Hallowed Fountain", "edition": None, "number": None, "section": "main"},
                    {"count": 4, "name": "Hinterland Harbor", "edition": None, "number": None, "section": "main"},
                    {"count": 4, "name": "Temple Garden", "edition": None, "number": None, "section": "main"},
                    {"count": 2, "name": "Temple of Mystery", "edition": None, "number": None, "section": "main"},
                    {"count": 3, "name": "Aether Gust", "edition": None, "number": None, "section": "main"},
                    {"count": 2, "name": "Knight of Autumn", "edition": None, "number": None, "section": "main"},
                    {"count": 2, "name": "Kraul Harpooner", "edition": None, "number": None, "section": "main"},
                    {"count": 3, "name": "Negate", "edition": None, "number": None, "section": "main"},
                    {
                        "count": 1,
                        "name": "Tamiyo, Collector of Tales",
                        "edition": None,
                        "number": None,
                        "section": "main",
                    },
                    {"count": 3, "name": "Time Wipe", "edition": None, "number": None, "section": "main"},
                    {
                        "count": 1,
                        "name": "Tolsimir, Friend to Wolves",
                        "edition": None,
                        "number": None,
                        "section": "main",
                    },
                ],
            }
        )
