# mtg-deck-finder

Attempts to find Magic The Gathering decks that can be built from an inventory.

No depenendencies.
Requires Python 3.6+

## Usage 

```
usage: mtg_deck_finder [-h] [-o {table,json,percent}] -i INVENTORY [deck]

attempts to find magic the gathering decks that can be built from an inventory

positional arguments:
  deck                  deck to compare against inventory

optional arguments:
  -h, --help            show this help message and exit
  -o {table,json,percent}, --output-format {table,json,percent}
                        output format, "table", "json" or "percent"
  -i INVENTORY, --inventory INVENTORY
                        inventory file of mtg cards available
```

e.g.

```
python -m mtg_deck_finder -i deck.dec -o json inventory.txt
```

## Examples

Process a folder of decks

```
find decks -iname *.dck -print -exec python3 -m mtg_deck_finder -i decks/inventory.txt -o percent "{}" \;
```
