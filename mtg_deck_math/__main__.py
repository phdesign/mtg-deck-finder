import json
from mtg_deck.deck_reader import DeckReader
from mtg_deck.writers.csv_deck_writer import CsvDeckWriter
from .config import Config


def main():
    config = Config()

    first = DeckReader(config.first, config.first.name).read()
    second = DeckReader(config.second, config.second.name).read()
    config.first.close()
    config.second.close()

    if config.operation == "add":
        result = first.add(second)
    else:
        result = first.subtract(second)

    CsvDeckWriter(config.outfile).write(result)
    config.outfile.close()


if __name__ == "__main__":
    main()
