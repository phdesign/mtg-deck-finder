import json
from mtg_deck.readers.csv_deck_reader import CsvDeckReader
from mtg_deck.deck_reader import DeckReader
from .fixtures import CSV_DECK, MTGTOP8_DECK

class TestCsvDeckReader:
    def test_should_read_all_cards_given_valid_csv(self):
        deck = DeckReader(CSV_DECK, "sample").read()
        assert json.dumps(deck.to_json()) == json.dumps({
            'name': "sample",
            'cards': [
                {"count": 2, "name": "Abomination of Gudul", "edition": "Khans of Tarkir", "number": 159, "section": "main"},
                {"count": 2, "name": "Abzan Banner", "edition": "Khans of Tarkir", "number": 215, "section": "main"},
                {"count": 1, "name": "Abzan Falconer", "edition": "Khans of Tarkir", "number": 2, "section": "main"},
                {"count": 2, "name": "Academy Drake", "edition": "Dominaria", "number": 40, "section": "main"},
                {"count": 3, "name": "Academy Journeymage", "edition": "Dominaria", "number": 41, "section": "main"},
                {"count": 1, "name": "Accumulated Knowledge", "edition": "Masters 25", "number": 40, "section": "main"},
                {"count": 1, "name": "Acid-Spewer Dragon", "edition": "Dragons of Tarkir", "number": 86, "section": "main"},
                {"count": 2, "name": "Act of Treason", "edition": "Khans of Tarkir", "number": 95, "section": "main"},
                {"count": 1, "name": "Adamant Will", "edition": "Dominaria", "number": 2, "section": "main"}
            ]
        })

    def test_should_be_able_to_read_given_valid_csv(self):
        can_read = CsvDeckReader(CSV_DECK, "sample").can_read()
        assert can_read

    def test_should_not_be_able_to_read_given_invalid_csv(self):
        can_read = CsvDeckReader(MTGTOP8_DECK, "sample").can_read()
        assert not can_read
