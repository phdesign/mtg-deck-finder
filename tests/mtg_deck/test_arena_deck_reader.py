# pylint: disable=attribute-defined-outside-init
import json
from mtg_deck.deck_reader import DeckReader

ARENA_DECK = """
1 Bristling Boar (M20) 338
2 Centaur Courser (M20) 168
3 Colossal Dreadmaw (M19) 172
1 Declare Dominance (M19) 175
10 Forest (M20) 279
4 Foul Orchard (M19) 251
1 Ghalta, Primal Hunger (RIX) 130
1 Gravewaker (M20) 323
2 Grazing Whiptail (XLN) 190
1 Greenwood Sentinel (M20) 174
2 Hitchclaw Recluse (GRN) 133
2 Impale (RIX) 76
1 Jungle Creeper (RIX) 161
3 Llanowar Elves (M19) 314
2 Moment of Craving (RIX) 79
1 Pelakka Wurm (M19) 192
1 Prodigious Growth (M19) 194
1 Ravenous Chupacabra (RIX) 82
2 Reclamation Sage (M19) 196
10 Swamp (M20) 272
2 Titanic Growth (M20) 343
2 Ursine Champion (M19) 304
2 Vampire Sovereign (M19) 125
1 Verdant Sun's Avatar (XLN) 213
1 Vigilant Baloth (M19) 206
1 Walking Corpse (M20) 327"""

class TestArenaDeckReader:

    def setup_method(self):
        deck_reader = DeckReader(ARENA_DECK, "sample")
        self.deck = deck_reader.read()

    def test_should_read_all_cards(self):
        assert json.dumps(self.deck.to_json()) == json.dumps([
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
        ])
