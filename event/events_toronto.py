# Toronto events
# Data source: https://www.toronto.ca/city-government/data-research-maps/open-data/open-data-catalogue/#21dd820d-dc7f-73d5-a6f0-6368b70a1b6f

from datetime import datetime
from typing import List

from bs4 import BeautifulSoup
import pandas as pd
import json

events = []

# XML file
with open('events_toronto.xml', 'r') as f:
    soup = BeautifulSoup(f, 'xml').find('viewentries')

for entry in soup.find_all('viewentry'):
    # Get raw data
    data_name = entry.find('entrydata', {'name': 'EventName'})
    data_area = entry.find('entrydata', {'name': 'Area'})
    data_date = entry.find('entrydata', {'name': 'DateBeginShow'})
    data_time = entry.find('entrydata', {'name': 'TimeBegin'})
    data_address = entry.find('entrydata', {'name': 'Address'})
    data_intersection = entry.find('entrydata', {'name': 'Intersection'})
    data_latitude = entry.find('entrydata', {'name': 'txtLat'})
    data_longitude = entry.find('entrydata', {'name': 'txtLong'})

    # Get actual data or 'NA'
    if data_date and data_time:
        # parse date
        date_parsed = None
        for fmt in ('%b %d, %Y', '%B %d, %Y'):
            try:
                date_parsed = datetime.strptime(data_date.get_text().strip(), fmt)
                break
            except ValueError:
                pass

        # parse time
        time_parsed = None
        try:
            time_parsed = datetime.strptime(data_time.get_text().strip(), '%H:%M %p')
        except ValueError:
            print(data_time.get_text().strip(), 'cannot be parsed')

        # parse hour: read from time_parsed, or try to split the time string, or simply assign 0
        try:
            hour = time_parsed.hour if time_parsed else int(data_time.get_text().split(':')[0].strip())
        except:
            hour = 'NA'

        if date_parsed:
            time = (date_parsed.year, date_parsed.month, date_parsed.day, hour)
            name, city_sector, address, intersection, latitude, longitude = tuple(
                map(lambda field: field.get_text().strip() if field else 'NA',
                    (data_name, data_area, data_address, data_intersection, data_latitude, data_longitude)))

            events.append(('Toronto', *time, name, city_sector, address, intersection, latitude, longitude))
        else:
            print(data_date.get_text().strip(), 'cannot be parsed')

# JSON file
with open('events_toronto.json', 'r') as f:
    json_data: List[dict] = json.load(f)

for obj in json_data:
    event: dict = obj.get('calEvent')
    if event:
        name = event.get('eventName')

        locations = []
        dates = []

        data_locations: List[dict] = event.get('locations')
        for data_location in data_locations:
            address = data_location.get('address')
            coords: dict = data_location.get('coords')

            if isinstance(coords, list):
                latitude = coords[0].get('lat') if coords else None
                longitude = coords[0].get('lng') if coords else None
            else:
                latitude = coords.get('lat') if coords else None
                longitude = coords.get('lng') if coords else None
            locations.append(('NA', address, 'NA', latitude, longitude))

        data_dates: List[dict] = event.get('dates')
        for data_date in data_dates:
            date_parsed = datetime.strptime(data_date.get('startDateTime'), '%Y-%m-%dT%H:%M:%S.%fZ')
            dates.append((date_parsed.year, date_parsed.month, date_parsed.day, date_parsed.hour))

        for location in locations:
            for date in dates:
                events.append(('Toronto', *date, name, *location))

df = pd.DataFrame(list(set(events)),
                  columns=['city', 'year', 'month', 'day', 'hour', 'title', 'city_sector', 'address', 'intersection',
                           'latitude', 'longitude'])
df.to_csv('events_toronto.csv')
