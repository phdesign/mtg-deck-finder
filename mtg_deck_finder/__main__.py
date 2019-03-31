from .config import Config
from .deck import DeckReader

def main():
    config = Config()

    deck_str = config.deck.read()
    config.deck.close()
    config.inventory.close()

    deck = DeckReader(deck_str).read()
    print(deck)

if __name__ == '__main__':
    main()
