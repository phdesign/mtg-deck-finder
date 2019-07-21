import os
import json
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

    if config.output_format == config.CSV:
        CsvDeckWriter(config.outfile).write(result)
    elif config.output_format == config.JSON:
        json_deck = json.dumps(result.to_json(), indent=4)
        config.outfile.write(json_deck)
    elif config.output_format == config.COUNT:
        total_count = sum(x.count for x in result)
        config.outfile.write(str(total_count) + os.linesep)
    config.outfile.close()


if __name__ == "__main__":
    main()
