#!/usr/bin/env python3

from pprint import pprint
import os
import sys
import csv
import requests
import requests_cache


API_KEY = os.environ['GOOGLE_API_KEY']
ENCODING = 'iso-8859-1'
#requests_cache.install_cache(cache_name='googleapi_cache', backend='sqlite', expire_after=None)


def make_lookup_phrase(row):
    """Return full name and address for google geo api text search."""
    address_text = "{} {}".format(row[1], row[2])
    return address_text


def call_google(address):
    """Return a dict with extracted fields from google response."""
    parameters = {'key': API_KEY, 'query': address}
    base = 'https://maps.googleapis.com/maps/api/place/textsearch/json'
    try:
        response = requests.get(base, params=parameters)
        answer = response.json()
        lat = answer['results'][0]['geometry']['location']['lat']
        lng = answer['results'][0]['geometry']['location']['lng']
        gname = answer['results'][0]['name']
        gaddress = answer['results'][0]['formatted_address']
    except IndexError:
        return {'gname': '', 'gaddress': '', 'lat': '', 'lng': ''}

    data_out = {'gname': gname, 'gaddress': gaddress, 'lat': lat, 'lng': lng}
    return data_out


def build_row(row, gdata):
    """Return a list of fields for csv writer."""
    lat = gdata.get('lat')
    lng = gdata.get('lng')
    gname = gdata.get('gname')
    gaddress = gdata.get('gaddress')

    row_out = [
        row[0],   # registration_number,
        row[1],   # premisses name
        row[2],   # address,
        row[3],   # classification,
        row[4],   # number_of_rooms,
        gname,    # Google Name
        gaddress, # Google Address
        lat,
        lng
    ]

    return row_out


def transform(file_in, file_out):
    """Creates a new csv file with added google name, address and lat lng columns."""
    with open(file_in, newline='', encoding=ENCODING) as csvfile:
        hotel_reader = csv.reader(csvfile, delimiter=',')
        next(hotel_reader)  #  bypass column names from original csv file

        with open(file_out, 'w', newline='', encoding=ENCODING) as csv_out:
            fieldnames = [ 'Registration Number', 'Premises Name', 'Address',
                           'Classification', 'Total Number Rooms',
                           'Google Name', 'Google Address',
                           'Lat', 'Lng']
            hotel_writer = csv.writer(csv_out, delimiter=',', quoting=csv.QUOTE_MINIMAL)
            hotel_writer.writerow(fieldnames)

            for row in hotel_reader:
                address = make_lookup_phrase(row)
                gdata = call_google(address)       # request to google geo text search
                new_row = build_row(row, gdata)
                hotel_writer.writerow(new_row)
                print(new_row)


def main(argv):
    transform(sys.argv[1], sys.argv[2])


if __name__=="__main__":
    if len(sys.argv) < 3:
        sys.exit("Usage: {} <sanitized_file_in.csv>, <file_out.csv>".format(sys.argv[0]))

    if not os.path.exists(sys.argv[1]):
        sys.exit("Error: {} file was not found!".format(sys.argv[1]))

    sys.exit(main(sys.argv))

