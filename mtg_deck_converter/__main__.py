from mtg_deck.deck_reader import DeckReader
from mtg_deck.writers.csv_deck_writer import CsvDeckWriter
from .config import Config


def main():
    config = Config()

    deck_str = config.deck.read()
    config.deck.close()

    deck = DeckReader(deck_str, config.deck.name).read()
    CsvDeckWriter(config.outfile).write(deck)


if __name__ == "__main__":
    main()
