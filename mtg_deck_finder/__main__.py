from functools import reduce
import collections
from .deck import DeckReader
from .config import Config

ComparisonEntry = collections.namedtuple('ComparisonEntry', ['name', 'deck_count', 'inventory_count'])

def compare(deck, inventory):
    cards = [ComparisonEntry(
        name=e.name,
        deck_count=e.count,
        inventory_count=next((i.count for i in inventory if i.name == e.name), 0)
    ) for e in deck]
    return cards

def print_percent(cards):
    matching_count = sum(c.inventory_count for c in cards)
    print(round((matching_count / len(cards)) * 100, 2))

def print_table(cards):
    """
---------------------------------------------------
Card         Deck Count   Inventory Count   Needed
---------------------------------------------------
Arena        4            2                 2
Werebear     1            0                 1
---------------------------------------------------
Total        60           2                 3
Similarity: 10%
    """
    header = {
        'name': 'Card',
        'deck_count': 'Deck Count',
        'inventory_count': 'Inventory Count',
        'needed': 'Needed'
    }
    rows = [{**c._asdict(), 'needed': c.deck_count - c.inventory_count} for c in cards]
    # print([header, *rows])
    widths = reduce(lambda acc, card: {
        'name': max(acc['name'], len(card['name'])),
        'deck_count': max(acc['deck_count'], len(str(card['deck_count']))),
        'inventory_count': max(acc['inventory_count'], len(str(card['inventory_count']))),
        'needed': max(acc['needed'], len(str(card['needed'])))
    }, [header, *rows], {
        'name': 0,
        'deck_count': 0,
        'inventory_count': 0,
        'needed': 0
    })
    template = "{{name:{name}}}  {{deck_count:{deck_count}}}  {{inventory_count:{inventory_count}}}  {{needed:{needed}}}" \
        .format(**widths)

    print('-' * 6)
    print(template.format(**header))
    print('-' * 6)
    for row in rows:
        print(template.format(**row))
    print('-' * 6)

def main():
    config = Config()

    deck_str = config.deck.read()
    inventory_str = config.inventory.read()
    config.deck.close()
    config.inventory.close()

    deck = DeckReader(deck_str).read()
    inventory = DeckReader(inventory_str).read()
    cards = compare(deck, inventory)

    if config.output_format == config.FORMAT_TABLE:
        print_table(cards)
    elif config.output_format == config.FORMAT_PERCENT:
        print_percent(cards)

if __name__ == '__main__':
    main()
