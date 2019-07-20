from io import StringIO
from mtg_deck.deck import Deck, DeckEntry
from mtg_deck.writers.csv_deck_writer import CsvDeckWriter
from .fixtures import CSV_OUTPUT

class TestCsvDeckWriter:
    def test_should_write_deck_to_csv_file(self):
        deck = Deck((DeckEntry(**x) for x in [
            {"count": 2, "name": "Abomination of Gudul", "edition": "Khans of Tarkir", "number": 159, "section": "main"},
            {"count": 2, "name": "Abzan Banner", "edition": "Khans of Tarkir", "number": 215, "section": "main"},
            {"count": 1, "name": "Abzan Falconer", "edition": "Khans of Tarkir", "number": 2, "section": "main"},
            {"count": 2, "name": "Academy Drake", "edition": "Dominaria", "number": 40, "section": "main"},
            {"count": 3, "name": "Academy Journeymage", "edition": "Dominaria", "number": 41, "section": "main"},
            {"count": 1, "name": "Accumulated Knowledge", "edition": "Masters 25", "number": 40, "section": "main"},
            {"count": 1, "name": "Acid-Spewer Dragon", "edition": "Dragons of Tarkir", "number": 86, "section": "main"},
            {"count": 2, "name": "Act of Treason", "edition": "Khans of Tarkir", "number": 95, "section": "main"},
            {"count": 1, "name": "Adamant Will", "edition": "Dominaria", "number": 2, "section": "main"}
        ]), name="sample")
        outfile = StringIO()
        CsvDeckWriter(outfile).write(deck)
        assert outfile.getvalue() == CSV_OUTPUT
