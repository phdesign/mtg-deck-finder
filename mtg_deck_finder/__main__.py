from .config import Config
from .deck import DeckReader, DeckEntry

def compare(deck, inventory):
    deck_count = 0
    missing_cards = []
    too_few_cards = []
    for deck_entry in deck:
        deck_count += deck_entry.count
        inventory_entry = next((e for e in inventory if e.name == deck_entry.name), None)
        if not inventory_entry:
            missing_cards.append(deck_entry)
        else:
            difference = deck_entry.count - inventory_entry.count
            if difference > 0:
                too_few_cards.append(DeckEntry(count=difference, name=deck_entry.name))

    missing_count = sum(e.count for e in missing_cards + too_few_cards)
    return {
        'deck_count': deck_count,
        'similarity': round(((deck_count - missing_count) / deck_count) * 100, 2),
        'missing_cards': missing_cards,
        'too_few_cards': too_few_cards
    }

def main():
    config = Config()

    deck_str = config.deck.read()
    inventory_str = config.inventory.read()
    config.deck.close()
    config.inventory.close()

    deck = DeckReader(deck_str).read()
    inventory = DeckReader(inventory_str).read()
    similarity = compare(deck, inventory)
    print(similarity)

if __name__ == '__main__':
    main()
