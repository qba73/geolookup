#!/usr/bin/env python

from pprint import pprint
import os
import csv
import requests


APIKEY = os.environ["GOOGLE_API_KEY"]
GOOGLE_URL = "https://maps.googleapis.com/maps/api/place/textsearch/json"


def make_lookup_phrase(row):
    add1, add2 = map(row.get, ('Premises Name', 'Address'))
    address_text = "{} {}".format(add1, add2)
    return address_text


def construct_row(row):
    registration_number = row.get('Registration Number')
    premises_name = row.get('Premises Name')
    address = row.get('Address')
    classification = row.get('Classification')
    rooms = row.get('Total Number Rooms')

    row_out = {
        'Registration Number': registation_number,
        'Premises Name': premisses_name,
        'Address': address,
        'Classification': classification,
        'Total Number Rooms': rooms
    }

    return row_out


def send_geo_request(phrase, url=GOOGLE_URL, api_key=API_KEY):
    params = {'key': api_key, 'query': phrase}
    res = requests.get(url, params=params)
    if res.status
    return res.json()


def extract_data(res):
    item = res.get('results')[0]
    name = item.get('name')
    address = item.get('formatted_address')
    lat = item.get('geometry').get('location').get('lat')
    lng = item.get('geometry').get('location').get('lng')
    d_out = {'Name': name, 'Address': address, 'lat': lat, 'lng': lng}
    return d_out


def construct_row_from_google_response(row, extdata):
    registration_number = row.get('Registration Number')
    name = extdata.get('Name')
    address = extdata.get('Address')
    classification = row.get('Classification')
    number_of_rooms = row.get('Total Number Rooms')
    lat = extdata.get('lat')
    lng = extdata.get('lng')

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
    with open('geohotels.csv', 'rb') as csvfile:
        hotel_reader = csv.DictReader(csvfile, delimiter=',')

        with open('google_hotels.csv', 'wb') as csv_out:
            fieldnames = ['Registration Number', 'Premises Name', 'Address', 'Classification', 'Total Number Rooms', 'Lat', 'Lng']
            hotel_writer = csv.DictWriter(csv_out, fieldnames=fieldnames, quoting=csv.QUOTE_MINIMAL)
            hotel_writer.writeheader()


            for row in hotel_reader:
                lookup_phrase = make_lookup_phrase(row)
                print("Google lookup phrase: {}".format(lookup_phrase))
                r = send_geo_request(lookup_phrase)
                gdata = extract_data(r)
                new_row = construct_row_from_google_response(row, gdata)
                hotel_writer.writerow(new_row)


def main():
    """
    1. open incsv
    2. for each row:
        - try to get google
    """ 
    pass


def send_request(address):
    pass


if __name__=="__main__":
    #if len(sys.argv < 3):
    #    sys.exit("Usage: {} <sanitized_file_in.csv>, <file_out.csv>".format(sys.argv[0]))
    #
    #sys.exit(main(sys.argv[1], sys.argv[2]))
    send_request()
