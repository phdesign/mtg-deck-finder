import json
from io import StringIO
from mtg_deck.deck_reader import DeckReader
from .fixtures import ARENA_DECK


class TestArenaDeckReader:
    def test_should_read_all_cards(self):
        deck = DeckReader(StringIO(ARENA_DECK), "sample").read()
        assert json.dumps(deck.to_json()) == json.dumps(
            {
                "name": "sample",
                "cards": [
                    {
                        "count": 1,
                        "name": "Bristling Boar",
                        "edition": "Core Set 2020",
                        "number": 338,
                        "section": "main",
                    },
                    {
                        "count": 2,
                        "name": "Centaur Courser",
                        "edition": "Core Set 2020",
                        "number": 168,
                        "section": "main",
                    },
                    {
                        "count": 3,
                        "name": "Colossal Dreadmaw",
                        "edition": "Core Set 2019",
                        "number": 172,
                        "section": "main",
                    },
                    {
                        "count": 1,
                        "name": "Declare Dominance",
                        "edition": "Core Set 2019",
                        "number": 175,
                        "section": "main",
                    },
                    {"count": 10, "name": "Forest", "edition": "Core Set 2020", "number": 279, "section": "main"},
                    {"count": 4, "name": "Foul Orchard", "edition": "Core Set 2019", "number": 251, "section": "main"},
                    {
                        "count": 1,
                        "name": "Ghalta, Primal Hunger",
                        "edition": "Rivals of Ixalan",
                        "number": 130,
                        "section": "main",
                    },
                    {"count": 1, "name": "Gravewaker", "edition": "Core Set 2020", "number": 323, "section": "main"},
                    {"count": 2, "name": "Grazing Whiptail", "edition": "Ixalan", "number": 190, "section": "main"},
                    {
                        "count": 1,
                        "name": "Greenwood Sentinel",
                        "edition": "Core Set 2020",
                        "number": 174,
                        "section": "main",
                    },
                    {
                        "count": 2,
                        "name": "Hitchclaw Recluse",
                        "edition": "Guilds of Ravnica",
                        "number": 133,
                        "section": "main",
                    },
                    {"count": 2, "name": "Impale", "edition": "Rivals of Ixalan", "number": 76, "section": "main"},
                    {
                        "count": 1,
                        "name": "Jungle Creeper",
                        "edition": "Rivals of Ixalan",
                        "number": 161,
                        "section": "main",
                    },
                    {
                        "count": 3,
                        "name": "Llanowar Elves",
                        "edition": "Core Set 2019",
                        "number": 314,
                        "section": "main",
                    },
                    {
                        "count": 2,
                        "name": "Moment of Craving",
                        "edition": "Rivals of Ixalan",
                        "number": 79,
                        "section": "main",
                    },
                    {"count": 1, "name": "Pelakka Wurm", "edition": "Core Set 2019", "number": 192, "section": "main"},
                    {
                        "count": 1,
                        "name": "Prodigious Growth",
                        "edition": "Core Set 2019",
                        "number": 194,
                        "section": "main",
                    },
                    {
                        "count": 1,
                        "name": "Ravenous Chupacabra",
                        "edition": "Rivals of Ixalan",
                        "number": 82,
                        "section": "main",
                    },
                    {
                        "count": 2,
                        "name": "Reclamation Sage",
                        "edition": "Core Set 2019",
                        "number": 196,
                        "section": "main",
                    },
                    {"count": 10, "name": "Swamp", "edition": "Core Set 2020", "number": 272, "section": "main"},
                    {
                        "count": 2,
                        "name": "Titanic Growth",
                        "edition": "Core Set 2020",
                        "number": 343,
                        "section": "main",
                    },
                    {
                        "count": 2,
                        "name": "Ursine Champion",
                        "edition": "Core Set 2019",
                        "number": 304,
                        "section": "main",
                    },
                    {
                        "count": 2,
                        "name": "Vampire Sovereign",
                        "edition": "Core Set 2019",
                        "number": 125,
                        "section": "main",
                    },
                    {"count": 1, "name": "Verdant Sun's Avatar", "edition": "Ixalan", "number": 213, "section": "main"},
                    {
                        "count": 1,
                        "name": "Vigilant Baloth",
                        "edition": "Core Set 2019",
                        "number": 206,
                        "section": "main",
                    },
                    {
                        "count": 1,
                        "name": "Walking Corpse",
                        "edition": "Core Set 2020",
                        "number": 327,
                        "section": "sideboard",
                    },
                ],
            }
        )
