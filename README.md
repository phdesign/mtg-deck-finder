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
  -f {table,json,percent}, --output-format {table,json,percent}
                        output format, "table", "json" or "percent"
  -i INVENTORY, --inventory INVENTORY
                        inventory file of mtg cards available
```

e.g.

```
python -m mtg_deck_finder -i inventory.txt -f json deck.dec
```

## Examples

Process a folder of decks

```
find decks -iname *.dck -print -exec python3 -m mtg_deck_finder -i decks/inventory.txt -f percent "{}" \;
```

Without filter

```
find decks -print -exec mtg-deck-finder -i decks/inventory.txt -f percent "{}" \; > decks/results_no_filter.csv
```

One result per line

```
find decks -iname '*.txt' -print -exec python3 -m mtg_deck_finder -i decks/inventory.txt -f percent "{}" \; | sed 'N;s/\(.*\)\n\(.*\)/\2 \1/'
```

Order by similarity

```
ag --nonumbers '^\d+' mtgtop8_result.txt | sort -r -n | head -n 10
```

Sort results from vim

```
# Delete failed files
:g/\D$\n\D/d
# Quote the filename
:%s/\v^((decks)\@=.*)$/"\1"/g
# Join lines with comma
:%s/\v([a-zA-Z])"\n/\1", /g 
```
