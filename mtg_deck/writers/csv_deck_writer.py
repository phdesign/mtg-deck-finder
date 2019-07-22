import os
import csv


class CsvDeckWriter:
    FIELDNAMES = ["Count", "Name", "Edition", "Card Number", "Section"]

    def __init__(self, outfile):
        self.outfile = outfile

    def write(self, deck):
        writer = csv.writer(self.outfile, lineterminator=os.linesep)

        writer.writerow(CsvDeckWriter.FIELDNAMES)
        writer.writerows([item.count, item.name, item.edition, item.number, item.section] for item in deck)
