from functools import reduce
import itertools
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

def calc_similarity(cards):
    matching_count = sum(c.inventory_count for c in cards)
    deck_count = sum(c.deck_count for c in cards)
    return round((matching_count / deck_count) * 100, 2)

def print_percent(cards):
    print(calc_similarity(cards))

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
    rows = [{**c._asdict(), 'needed': max(c.deck_count - c.inventory_count, 0)} for c in cards]
    totals = reduce(lambda acc, c: {
        'name': 'Total',
        'deck_count': acc['deck_count'] + c['deck_count'],
        'inventory_count': acc['inventory_count'] + c['inventory_count'],
        'needed': acc['needed'] + c['needed']
    }, rows)
    col_lengths = ((len(str(v)) for v in card.values()) for card in [header, *rows])
    widths = list(map(max, zip(*col_lengths)))
    template = "{{name:{0}}}  {{deck_count:{1}}}  {{inventory_count:{2}}}  {{needed:{3}}}" \
        .format(*widths)
    line_length = sum(widths) + 6
    separator = '-' * line_length

    print(separator)
    print(template.format(**header))
    print(separator)
    for row in rows:
        print(template.format(**row))
    print(separator)
    print(template.format(**totals))
    print("Similarity: {0}%".format(calc_similarity(cards)))

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
