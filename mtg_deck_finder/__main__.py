import sys
from mtg_deck.deck_reader import DeckReader
from mtg_deck.errors import DeckFormatNotSupportedError
from . import compare
from .config import Config


def main():
    config = Config()

    try:
        deck = DeckReader(config.deck, config.deck.name).read().exclude_metadata().normalise()
    except DeckFormatNotSupportedError:
        print('deck format not supported: ' + config.deck.name, file=sys.stderr)
        exit(1)
    finally:
        config.deck.close()

    try:
        inventory = DeckReader(config.inventory).read().exclude_metadata().normalise()
    except DeckFormatNotSupportedError:
        print('inventory deck format not supported', file=sys.stderr)
        exit(1)
    finally:
        config.inventory.close()

    comparison = compare.compare(deck, inventory)

    if config.output_format == config.FORMAT_TABLE:
        compare.print_table(comparison)
    elif config.output_format == config.FORMAT_JSON:
        compare.print_json(comparison)
    else:
        compare.print_percent(comparison)


if __name__ == "__main__":
    main()
