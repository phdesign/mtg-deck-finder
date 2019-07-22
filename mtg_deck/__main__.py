import os
import json
from .deck_reader import DeckReader
from .writers.csv_deck_writer import CsvDeckWriter
from .config import Config


def transform(operation, deck, other=None):
    if operation == Config.NORMALISE:
        return deck.normalise()

    if operation == Config.NO_SIDEBOARD:
        return deck.without_sideboard()

    if operation == Config.STRIP_META:
        return deck.exclude_metadata()

    if operation == Config.ADD:
        return deck.add(other)

    if operation == Config.SUBTRACT:
        return deck.subtract(other)

    if operation == Config.SORT:
        deck.sort()

    return deck


def main():
    config = Config()

    deck = DeckReader(config.deck, config.deck.name).read()
    config.deck.close()

    if config.other:
        other = DeckReader(config.other, config.other.name).read()
        config.other.close()

    for operation in config.operations:
        if operation in [Config.ADD, Config.SUBTRACT]:
            deck = transform(operation, deck, other)
            break
        deck = transform(operation, deck)
        if config.other:
            other = transform(operation, other)

    if config.output_format == config.CSV:
        CsvDeckWriter(config.outfile).write(deck)
    elif config.output_format == config.JSON:
        json_deck = json.dumps(deck.to_json(), indent=4)
        config.outfile.write(json_deck)
    elif config.output_format == config.COUNT:
        total_count = sum(x.count for x in deck)
        config.outfile.write(str(total_count) + os.linesep)
    config.outfile.close()


if __name__ == "__main__":
    main()
