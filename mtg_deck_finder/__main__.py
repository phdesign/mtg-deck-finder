from .config import Config
from .deck import DeckReader, DeckEntry

def compare(deck, inventory):
    deck_set = set(deck)
    inventory_set = set(inventory)

    not_in_inventory = deck_set - inventory_set
    intersection = deck_set & inventory_set
    print(intersection)
    # difference = [c for c in intersection]

def main():
    config = Config()

    deck_str = config.deck.read()
    inventory_str = config.inventory.read()
    config.deck.close()
    config.inventory.close()

    deck = DeckReader(deck_str).read()
    inventory = DeckReader(inventory_str).read()
    compare(deck, inventory)

if __name__ == '__main__':
    main()
