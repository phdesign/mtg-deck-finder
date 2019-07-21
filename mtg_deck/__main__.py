from .deck_reader import DeckReader
from .writers.csv_deck_writer import CsvDeckWriter
from .config import Config


def main():
    config = Config()

    result = DeckReader(config.deck, config.deck.name).read()
    config.deck.close()

    if config.operation in [config.ADD, config.SUBTRACT]:
        other = DeckReader(config.other, config.other.name).read()
        config.other.close()
        if config.operation == config.ADD:
            result = result.add(other)
        elif config.operation == config.SUBTRACT:
            result = result.subtract(other)

    elif config.operation == config.NORMALISE:
        result = result.normalise()

    elif config.operation == config.NO_SIDEBOARD:
        result = result.without_sideboard()

    elif config.operation == config.STRIP_META:
        result = result.exclude_metadata()

    CsvDeckWriter(config.outfile).write(result)
    config.outfile.close()


if __name__ == "__main__":
    main()
