from mtg_deck.deck_reader import DeckReader
from . import compare
from .config import Config


def main():
    config = Config()

    deck = DeckReader(config.deck, config.deck.name).read().exclude_metadata().normalise()
    inventory = DeckReader(config.inventory).read().exclude_metadata().normalise()
    config.deck.close()
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
