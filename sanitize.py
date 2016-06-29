#!/usr/bin/env python3


import csv
import os
import sys


ENCODING = 'iso-8859-1'
FIELDNAMES = ['Registration Number', 'Premises Name', 'Address', 'Classification', 'Total Number Rooms', 'Lat', 'Lng']


def make_address(row):
    address_text = "{} {} {} Ireland".format(row[3], row[4], row[5])
    return address_text


def build_row(row):
    """Return a list with field names for new csv file."""
    address = make_address(row)
    el1 = row[0]  #Registration Number
    el2 = row[1]  #Premises Name
    el4 = row[2]  #Classification
    el5 = row[7]  #Total Number Rooms
    row_out = [el1, el2, address, el4, el5]
    return row_out


def main(argv):
    with open(argv[1], newline='', encoding=ENCODING) as csvfile:
        hotel_reader = csv.reader(csvfile, delimiter=',')
        next(hotel_reader)  # bypass original csv header in the source csv file

        with open(argv[2], 'w', newline='') as csv_out:
            fieldnames = FIELDNAMES
            hotel_writer = csv.writer(csv_out, delimiter=',')
            hotel_writer.writerow(FIELDNAMES)

            for row in hotel_reader:
                r = build_row(row)
                hotel_writer.writerow(r)


if __name__=="__main__":
    if len(sys.argv) < 3:
        sys.exit("Usage: {} <file_in.csv> <file_out.csv>".format(sys.argv[0]))

    if not os.path.exists(sys.argv[1]):
        sys.exit("Error: {} file was not found!".format(sys.argv[1]))


    sys.exit(main(sys.argv))

