# GeoLookup
Simple Python utilities for adding positioning information to addresses stored in a csv file.
## Requirements
The tool utilizes Google Places API Web Service. In order to use the API it is required to register in google developers program and to generate API key. 
## How to configure the environment
> **Preconditions:**
> - installed python [virtualenv](https://pypi.python.org/pypi/virtualenv)
> - generated and exported GOOGLE_API_KEY for interaction with [Google Web Services](https://developers.google.com/places/web-service/)

- create and cativate python virtual environment
```bash
$ virtualenv venv-geo
$ source venv-geo/bin/activate
``` 
- install dependencies
```bash
$ pip install -r requirements.txt
```
## Preparing data
Structure of the original CSV file:
```csv
Registration Number,Premises Name,Classification,Address 1,Address 2,County,Registered Owner,Total Number Rooms
XYZ04166,Moycarn Lodge and Marina,3 Star,Shannonbridge Road Ballinasloe,Church Street,Ballinasloe,Joe and Fiona Melody,15
```
Run **sanitize.py**
```bash
$ ./sanitize.py 
Usage: ./sanitize.py <file_in.csv> <file_out.csv>
```
Outcome csv file will look like this:
```csv
Registration Number,Premises Name,Address,Classification,Total Number Rooms
XYZ04416,Moycarn Lodge and Marina,Shannonbridge Road Ballinasloe Church Street Ballinasloe Ireland,3 Star,15
```
##Adding location to records
Run **hotels.py**
```bash
$ ./hotels.py 
Usage: ./hotels.py <sanitized_file_in.csv>, <file_out.csv>
```
Outcome csv file will look like this:
```csv
Registration Number,Premises Name,Address,Classification,Total Number Rooms,Lat,Lng
XYZ03863,Glenlo Abbey Hotel,Bushy Park Galway. Co Galway Ireland,5 Star,49,53.300406,-9.098559
```
> **Note:**
> When Google Web Service is not able to recognize requested premises, csv outcome file will contain empty string.

Example record with not recognized address:
```csv
XYZ01430,Marine Hotel,"The Pier Glandore, R597 Co Cork Ireland",2 Star,11,,
```

