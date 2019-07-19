# pylint: disable=attribute-defined-outside-init
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

class TestApprenticeDeckReader:

    def setup_method(self):
        deck_reader = DeckReader(APPRENTICE_DECK, "sample")
        self.deck = deck_reader.read()

    def test_should_return_all_cards_given_apprentice_file(self):
        assert len(self.deck) == 22

    def test_should_return_card_count_given_apprentice_file(self):
        assert sum(e.count for e in self.deck) == 75

    def test_should_return_card_in_main_section_given_apprentice_file(self):
        assert any(e.name == "Anger of the Gods" for e in self.deck)

    def test_should_return_card_in_sideboard_section_given_apprentice_file(self):
        assert any(e.name == "Trinisphere" for e in self.deck)

class TestApprenticeDeckReaderWithoutSideboard:

    def setup_method(self):
        deck_reader = DeckReader(APPRENTICE_DECK, "sample")
        self.deck = deck_reader.read().without_sideboard()

    def test_should_return_all_main_cards_given_apprentice_file_without_sideboard(self):
        assert len(self.deck) == 15

    def test_should_return_card_count_given_apprentice_file_without_sideboard(self):
        assert sum(e.count for e in self.deck) == 60

    def test_should_return_card_in_main_section_given_apprentice_file_without_sideboard(self):
        assert any(e.name == "Anger of the Gods" for e in self.deck)

    def test_should_not_return_card_in_sideboard_section_given_apprentice_file_without_sideboard(self):
        assert not any(e.name == "Trinisphere" for e in self.deck)

class TestSimpleDeckReader:

    def setup_method(self):
        deck_reader = DeckReader(MTGTOP8_DECK, "sample")
        self.deck = deck_reader.read()

    def test_should_return_all_cards_given_mtgtop8_file(self):
        assert len(self.deck) == 27

    def test_should_return_card_count_given_mtgtop8_file(self):
        assert sum(e.count for e in self.deck) == 75

    def test_should_return_card_in_main_section_given_mtgtop8_file(self):
        assert any(e.name == "Vivid Creek" for e in self.deck)

    def test_should_return_card_in_sideboard_section_given_mtgtop8_file(self):
        assert any(e.name == "Negate" for e in self.deck)

class TestSimpleDeckReaderWithoutSideboard:

    def setup_method(self):
        deck_reader = DeckReader(MTGTOP8_DECK, "sample")
        self.deck = deck_reader.read().without_sideboard()

    def test_should_return_all_main_cards_given_mtgtop8_file_without_sideboard(self):
        assert len(self.deck) == 19

    def test_should_return_card_count_given_mtgtop8_file_without_sideboard(self):
        assert sum(e.count for e in self.deck) == 60

    def test_should_return_card_in_main_section_given_mtgtop8_file_without_sideboard(self):
        assert any(e.name == "Vivid Creek" for e in self.deck)

    def test_should_not_return_card_in_sideboard_section_given_mtgtop8_file_without_sideboard(self):
        assert not any(e.name == "Negate" for e in self.deck)
