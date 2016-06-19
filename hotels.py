#!/usr/bin/env python

from pprint import pprint
import os
import csv
import requests


API_KEY = os.environ["GOOGLE_API_KEY"]
GOOGLE_URL = "https://maps.googleapis.com/maps/api/place/textsearch/json"


def make_lookup_phrase(row):
    add1, add2 = map(row.get, ('Premises Name', 'Address'))
    address_text = "{} {}".format(add1, add2)
    return address_text


def make_address(row):
    add1, add2, add3 = map(row.get, ('Address 1', 'Address 2', 'County'))
    address_text = "{} {} {} Ireland".format(add1, add2, add3)
    return address_text


def construct_row(row):
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


def send_geo_request(phrase, url=GOOGLE_URL, api_key=API_KEY):
    params = {'key': api_key, 'query': phrase}
    res = requests.get(url, params=params)
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



with open('hotels.csv', 'rb') as csvfile:
    hotel_reader = csv.DictReader(csvfile, delimiter=',')
    
    with open('geohotels.csv', 'wb') as csv_out:
        fieldnames = ['Registration Number', 'Premises Name', 'Address', 'Classification', 'Total Number Rooms']
        hotel_writer = csv.DictWriter(csv_out, fieldnames=fieldnames)
        hotel_writer.writeheader()

        for row in hotel_reader:
            r = construct_row(row)
            hotel_writer.writerow(r)


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
    pass


if __name__=="__main__":
    main()
