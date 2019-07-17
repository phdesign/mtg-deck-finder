import json
from functools import reduce
import collections
from mtg_deck.deck_reader import DeckReader
from .config import Config

def main():
    config = Config()

    first_str = config.first.read()
    second_str = config.second.read()
    config.first.close()
    config.second.close()

    first = DeckReader(first_str, config.first.name).read()
    second = DeckReader(second_str, config.second.name).read()

    print(first)
    print(second)

if __name__ == '__main__':
    main()
