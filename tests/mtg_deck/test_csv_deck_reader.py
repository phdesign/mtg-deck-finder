import json
from mtg_deck.deck_reader import DeckReader

CSV_DECK = """
Count,Tradelist Count,Name,Edition,Card Number,Condition,Language,Foil,Signed,Artist Proof,Altered Art,Misprint,Promo,Textless,My Price
2,0,Abomination of Gudul,Khans of Tarkir,159,Near Mint,English,,,,,,,,
2,0,Abzan Banner,Khans of Tarkir,215,Near Mint,English,,,,,,,,
1,0,Abzan Falconer,Khans of Tarkir,2,Near Mint,English,,,,,,,,0
2,0,Academy Drake,Dominaria,40,Near Mint,English,,,,,,,,
3,0,Academy Journeymage,Dominaria,41,Near Mint,English,,,,,,,,
1,0,Accumulated Knowledge,Masters 25,40,Near Mint,English,,,,,,,,
1,0,Acid-Spewer Dragon,Dragons of Tarkir,86,Near Mint,English,,,,,,,,
2,0,Act of Treason,Khans of Tarkir,95,Near Mint,English,,,,,,,,0
1,0,Adamant Will,Dominaria,2,Near Mint,English,,,,,,,,"""

class TestCsvDeckReader:

    def test_should_read_all_cards(self):
        deck_reader = DeckReader(CSV_DECK, "sample")
        deck = deck_reader.read()
        assert json.dumps(deck.to_json()) == json.dumps({
            'name': "sample",
            'cards': [
                { "count": 2, "name": "Abomination of Gudul", "edition": "Khans of Tarkir", "number": 158, "section": "main", },
            ]
        })
