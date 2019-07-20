import json
from io import StringIO
from mtg_deck.deck_reader import DeckReader
from .fixtures import ARENA_DECK

class TestArenaDeckReader:

    def test_should_read_all_cards(self):
        deck = DeckReader(StringIO(ARENA_DECK), "sample").read()
        assert json.dumps(deck.to_json()) == json.dumps({
            'name': "sample",
            'cards': [
                { "count": 1, "name": "Bristling Boar", "edition": "M20", "number": 338, "section": "main", },
                { "count": 2, "name": "Centaur Courser", "edition": "M20", "number": 168, "section": "main", },
                { "count": 3, "name": "Colossal Dreadmaw", "edition": "M19", "number": 172, "section": "main", },
                { "count": 1, "name": "Declare Dominance", "edition": "M19", "number": 175, "section": "main", },
                { "count": 10, "name": "Forest", "edition": "M20", "number": 279, "section": "main", },
                { "count": 4, "name": "Foul Orchard", "edition": "M19", "number": 251, "section": "main", },
                { "count": 1, "name": "Ghalta, Primal Hunger", "edition": "RIX", "number": 130, "section": "main", },
                { "count": 1, "name": "Gravewaker", "edition": "M20", "number": 323, "section": "main", },
                { "count": 2, "name": "Grazing Whiptail", "edition": "XLN", "number": 190, "section": "main", },
                { "count": 1, "name": "Greenwood Sentinel", "edition": "M20", "number": 174, "section": "main", },
                { "count": 2, "name": "Hitchclaw Recluse", "edition": "GRN", "number": 133, "section": "main", },
                { "count": 2, "name": "Impale", "edition": "RIX", "number": 76, "section": "main", },
                { "count": 1, "name": "Jungle Creeper", "edition": "RIX", "number": 161, "section": "main", },
                { "count": 3, "name": "Llanowar Elves", "edition": "M19", "number": 314, "section": "main", },
                { "count": 2, "name": "Moment of Craving", "edition": "RIX", "number": 79, "section": "main", },
                { "count": 1, "name": "Pelakka Wurm", "edition": "M19", "number": 192, "section": "main", },
                { "count": 1, "name": "Prodigious Growth", "edition": "M19", "number": 194, "section": "main", },
                { "count": 1, "name": "Ravenous Chupacabra", "edition": "RIX", "number": 82, "section": "main", },
                { "count": 2, "name": "Reclamation Sage", "edition": "M19", "number": 196, "section": "main", },
                { "count": 10, "name": "Swamp", "edition": "M20", "number": 272, "section": "main", },
                { "count": 2, "name": "Titanic Growth", "edition": "M20", "number": 343, "section": "main", },
                { "count": 2, "name": "Ursine Champion", "edition": "M19", "number": 304, "section": "main", },
                { "count": 2, "name": "Vampire Sovereign", "edition": "M19", "number": 125, "section": "main", },
                { "count": 1, "name": "Verdant Sun's Avatar", "edition": "XLN", "number": 213, "section": "main", },
                { "count": 1, "name": "Vigilant Baloth", "edition": "M19", "number": 206, "section": "main", },
                { "count": 1, "name": "Walking Corpse", "edition": "M20", "number": 327, "section": "main", }
            ]
        })
