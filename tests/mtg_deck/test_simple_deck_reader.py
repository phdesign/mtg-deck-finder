# pylint: disable=attribute-defined-outside-init
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

    def setup_method(self):
        deck_reader = DeckReader(MTGTOP8_DECK, "sample")
        self.deck = deck_reader.read()

    def test_should_return_all_cards(self):
        assert len(self.deck) == 27

    def test_should_return_card_count(self):
        assert sum(e.count for e in self.deck) == 75

    def test_should_return_card_in_main_section(self):
        assert any(e.name == "Vivid Creek" for e in self.deck)

    def test_should_return_card_in_sideboard_section(self):
        assert any(e.name == "Negate" for e in self.deck)

class TestSimpleDeckReaderWithoutSideboard:

    def setup_method(self):
        deck_reader = DeckReader(MTGTOP8_DECK, "sample")
        self.deck = deck_reader.read().without_sideboard()

    def test_should_return_all_main_cards_given_sideboard_is_excluded(self):
        assert len(self.deck) == 19

    def test_should_return_card_count_given_sideboard_is_excluded(self):
        assert sum(e.count for e in self.deck) == 60

    def test_should_return_card_in_main_section_given_sideboard_is_excluded(self):
        assert any(e.name == "Vivid Creek" for e in self.deck)

    def test_should_not_return_card_in_sideboard_section_given_sideboard_is_excluded(self):
        assert not any(e.name == "Negate" for e in self.deck)
