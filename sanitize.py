#!/usr/bin/env python


import csv
import os
import sys


FIELDNAMES = ['Registration Number', 'Premises Name', 'Address', 'Classification', 'Total Number Rooms', 'Lat', 'Lng']


def make_address(row):
    """Return premisses address as a string."""
    add1, add2, add3 = map(row.get, ('Address 1', 'Address 2', 'County'))
    address_text = "{} {} {} Ireland".format(add1, add2, add3)
    return address_text


def construct_row(row):
    """Return a dict with field names for new csv file."""
    address = make_address(row)
    el1 = row.get('Registration Number')
    el2 = row.get('Premises Name')
    el4 = row.get('Classification')
    el5 = row.get('Total Number Rooms')

    row_out = {
        'Registration Number': el1,
        'Premises Name': el2,
        'Address': address,
        'Classification': el4,
        'Total Number Rooms': el5
    }

    return row_out


def main(file_in, file_out):
    with open(file_in, 'rb') as csvfile:
        hotel_reader = csv.DictReader(csvfile, delimiter=',')

        with open(file_out, 'wb') as csv_out:
            fieldnames = FIELDNAMES
            hotel_writer = csv.DictWriter(csv_out, fieldnames=fieldnames)
            hotel_writer.writeheader()

            for row in hotel_reader:
                r = construct_row(row)
                hotel_writer.writerow(r)


if __name__=="__main__":
    if len(sys.argv) < 3:
        sys.exit("Usage: {} <file_in.csv> <file_out.csv>".format(sys.argv[0]))

    sys.exit(main(sys.argv[1], sys.argv[2]))

