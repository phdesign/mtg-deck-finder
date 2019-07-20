from mtg_deck.deck_reader import DeckReader
from mtg_deck.writers.csv_deck_writer import CsvDeckWriter
from .config import Config


def main():
    config = Config()

    deck = DeckReader(config.deck, config.deck.name).read()
    config.deck.close()
    CsvDeckWriter(config.outfile).write(deck)
    config.outfile.close()


if __name__ == "__main__":
    main()
