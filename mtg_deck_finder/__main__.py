import sys
import json
from functools import reduce
import collections
from .deck import DeckReader
from .config import Config

Comparison = collections.namedtuple('Comparison', ['cards', 'total', 'similarity'])

def compare(deck, inventory):
    cards = [{**c, 'needed': max(c['deck_count'] - c['inventory_count'], 0)} for c in ({
        'name': e.name,
        'deck_count': e.count,
        'inventory_count': next((i.count for i in inventory if i.name == e.name), 0)
    } for e in deck)]
    totals = reduce(lambda acc, c: {
        'name': 'Total',
        'deck_count': acc['deck_count'] + c['deck_count'],
        'inventory_count': "",
        'needed': acc['needed'] + c['needed']
    }, cards)
    matching_count = totals['deck_count'] - totals['needed']
    deck_count = sum(c['deck_count'] for c in cards)
    similarity = round((matching_count / deck_count) * 100, 2)
    return Comparison(
        cards=cards,
        total=totals,
        similarity=similarity
    )

def print_percent(comparison):
    print(comparison.similarity)

def print_table(comparison):
    """ Prints a table based view of the results, e.g.
--------------------------------------------------
Card         Deck Count   Inventory Count   Needed
--------------------------------------------------
Arena        4            2                 2
Werebear     1            0                 1
--------------------------------------------------
Total        60           2                 3
Similarity: 10%
    """
    header = {
        'name': 'Card',
        'deck_count': 'Deck Count',
        'inventory_count': 'Inventory Count',
        'needed': 'Needed'
    }
    col_lengths = ((len(str(v)) for v in card.values()) for card in [header, *comparison.cards, comparison.total])
    widths = list(map(max, zip(*col_lengths)))
    template = "{{name:{0}}}  {{deck_count:{1}}}  {{inventory_count:{2}}}  {{needed:{3}}}" \
        .format(*widths)
    line_length = sum(widths) + 6
    separator = '-' * line_length

    print(separator)
    print(template.format(**header))
    print(separator)
    for card in comparison.cards:
        print(template.format(**card))
    print(separator)
    print(template.format(**comparison.total))
    print("Similarity: {0}%".format(comparison.similarity))

def print_json(comparison):
    print(json.dumps(comparison._asdict()))

def main():
    config = Config()

    deck_str = config.deck.read()
    inventory_str = config.inventory.read()
    config.deck.close()
    config.inventory.close()

    deck = DeckReader(deck_str, config.deck.name).read()
    inventory = DeckReader(inventory_str).read()
    comparison = compare(deck, inventory)

    if config.output_format == config.FORMAT_TABLE:
        print_table(comparison)
    elif config.output_format == config.FORMAT_JSON:
        print_json(comparison)
    else:
        print_percent(comparison)

if __name__ == '__main__':
    main()
