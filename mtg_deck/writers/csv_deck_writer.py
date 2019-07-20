import csv

class CsvDeckWriter():
    def __init__(self, outfile):
        self.outfile = outfile

    def write(self, deck):
        fieldnames = ['Count', 'Name', 'Edition', 'Card Number', 'Section']
        writer = csv.writer(self.outfile, lineterminator="\n")

        writer.writerow(fieldnames)
        writer.writerows([
            item.count,
            item.name,
            item.edition,
            item.number,
            item.section
        ] for item in deck)
