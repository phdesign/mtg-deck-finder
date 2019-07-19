import json
from functools import reduce
import collections
from mtg_deck.deck_reader import DeckReader
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
    similarity = calc_similarity(cards)
    return Comparison(
        cards=cards,
        total=totals,
        similarity=similarity
    )

def calc_similarity(cards):
    """Calculate similarity, using an 80 / 20 rule.

    80% of the score goes to number of uniquely matched cards.
    20% of the score goes to duplicate matched cards.
    """
    unique_matches = sum(1 for c in cards if c['inventory_count'] > 0)
    unique_cards = len(cards)
    unique_score = unique_matches / unique_cards

    full_matches = sum(c['deck_count'] - c['needed'] for c in cards)
    deck_count = sum(c['deck_count'] for c in cards)
    full_score = full_matches / deck_count

    return round((unique_score * 0.8 + full_score * 0.2) * 100, 2)

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
    normalised_deck = deck.without_sideboard().normalise()
    normalised_inventory = inventory.normalise()
    comparison = compare(normalised_deck, normalised_inventory)

    if config.output_format == config.FORMAT_TABLE:
        print_table(comparison)
    elif config.output_format == config.FORMAT_JSON:
        print_json(comparison)
    else:
        print_percent(comparison)

if __name__ == '__main__':
    main()
