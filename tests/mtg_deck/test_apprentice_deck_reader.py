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

class TestApprenticeDeckReader:

    def setup_method(self):
        deck_reader = DeckReader(APPRENTICE_DECK, "sample")
        self.deck = deck_reader.read()

    def test_should_return_all_cards(self):
        assert len(self.deck) == 22

    def test_should_return_card_count(self):
        assert sum(e.count for e in self.deck) == 75

    def test_should_return_card_in_main_section(self):
        assert any(e.name == "Anger of the Gods" for e in self.deck)

    def test_should_return_card_in_sideboard_section(self):
        assert any(e.name == "Trinisphere" for e in self.deck)

class TestApprenticeDeckReaderWithoutSideboard:

    def setup_method(self):
        deck_reader = DeckReader(APPRENTICE_DECK, "sample")
        self.deck = deck_reader.read().without_sideboard()

    def test_should_return_all_main_cards_given_sideboard_is_excluded(self):
        assert len(self.deck) == 15

    def test_should_return_card_count_given_sideboard_is_excluded(self):
        assert sum(e.count for e in self.deck) == 60

    def test_should_return_card_in_main_section_given_sideboard_is_excluded(self):
        assert any(e.name == "Anger of the Gods" for e in self.deck)

    def test_should_not_return_card_in_sideboard_section_given_sideboard_is_excluded(self):
        assert not any(e.name == "Trinisphere" for e in self.deck)
