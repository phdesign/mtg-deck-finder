from mtg_deck.deck_reader import DeckReader
from . import compare
from .config import Config


def main():
    config = Config()

    deck = DeckReader(config.deck, config.deck.name).read()
    inventory = DeckReader(config.inventory).read()
    config.deck.close()
    config.inventory.close()

    normalised_deck = deck.without_sideboard().normalise()
    normalised_inventory = inventory.normalise()
    comparison = compare.compare(normalised_deck, normalised_inventory)

    if config.output_format == config.FORMAT_TABLE:
        compare.print_table(comparison)
    elif config.output_format == config.FORMAT_JSON:
        compare.print_json(comparison)
    else:
        compare.print_percent(comparison)


if __name__ == "__main__":
    main()
