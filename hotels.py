#!/usr/bin/env python

from pprint import pprint
import os
import sys
import csv
import requests
import requests_cache


API_KEY = os.environ['GOOGLE_API_KEY']
requests_cache.install_cache(cache_name='googleapi_cache', backend='sqlite', expire_after=None)


def make_lookup_phrase(row):
    """Return full name and address for google geo api text search."""
    add1, add2 = map(row.get, ('Premises Name', 'Address'))
    address_text = "{} {}".format(add1, add2)
    return address_text


def getlatlng(address):
    """Return lat lng of the requested address."""
    parameters = {'key': API_KEY, 'query': address}
    base = 'https://maps.googleapis.com/maps/api/place/textsearch/json'
    try:
        response = requests.get(base, params=parameters)
        answer = response.json()
        lat_lng = answer['results'][0]['geometry']['location']
    except IndexError:
        return {'lat': '', 'lng': ''}
    return lat_lng


def build_row(row, latlng):
    registration_number = row.get('Registration Number')
    name = row.get('Premises Name')
    address = row.get('Address')
    classification = row.get('Classification')
    number_of_rooms = row.get('Total Number Rooms')
    lat = latlng.get('lat')
    lng = latlng.get('lng')

    row_out = {
        'Registration Number': registration_number,
        'Premises Name': name,
        'Address': address,
        'Classification': classification,
        'Total Number Rooms': number_of_rooms,
        'Lat': lat,
        'Lng': lng
    }

    return row_out


def transform(file_in, file_out):
    """Creates a new csv file with added lat lng columns."""
    with open(file_in, 'rb') as csvfile:
        hotel_reader = csv.DictReader(csvfile, delimiter=',')

        with open(file_out, 'wb') as csv_out:
            fieldnames = [
                'Registration Number', 'Premises Name',
                'Address', 'Classification',
                'Total Number Rooms', 'Lat', 'Lng'
            ]
            hotel_writer = csv.DictWriter(csv_out,
                                          fieldnames=fieldnames,
                                          quoting=csv.QUOTE_MINIMAL)
            hotel_writer.writeheader()

            for row in hotel_reader:
                address = make_lookup_phrase(row)
                print("Google lookup phrase: {}".format(address))
                latlng = getlatlng(address)       # request to google geo text search
                new_row = build_row(row, latlng)
                hotel_writer.writerow(new_row)


def main(argv):
    transform(sys.argv[1], sys.argv[2])


if __name__=="__main__":
    if len(sys.argv) < 3:
        sys.exit("Usage: {} <sanitized_file_in.csv>, <file_out.csv>".format(sys.argv[0]))

    if not os.path.exists(sys.argv[1]):
        sys.exit("Error: {} file was not found!".format(sys.argv[1]))

    sys.exit(main(sys.argv))

