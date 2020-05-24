# Ottawa events
# Data source: http://data.ottawa.ca/dataset/spotlight-ottawa-gatineau-events-calendar/resource/43d50cc3-0c5b-4901-91f7-9d425feaf97e

from datetime import datetime

from bs4 import BeautifulSoup
import pandas as pd

with open('events.xml', 'r') as f:
    soup = BeautifulSoup(f, 'xml')

events = []

for event in soup.find_all('event'):
    date = datetime.strptime(event.start_date.get_text(), '%Y%m%d%H%M%S')
    year, month, day = date.year, date.month, date.day
    title = event.title_english.get_text()
    city_sector = event.city_sector.title_english.get_text() if event.city_sector and event.city_sector.title_english else 'NA'
    if event.locations:
        locations = [
            (location.address_english.get_text() if location.address_english else 'NA',
             location.intersection_english.get_text() if location.intersection_english else 'NA',
             location.postal_code.get_text() if location.postal_code else 'NA')
            for location in event.locations.find_all('location')]
        for location in locations:
            # Event data doesn't have precise hour, so assign 'NA' for every event
            events.append(('Ottawa', year, month, day, 'NA', title, city_sector, *location))

df = pd.DataFrame(events,
                  columns=['city', 'year', 'month', 'day', 'hour', 'title', 'city_sector', 'address', 'intersection',
                           'postal_code'])
df.to_csv('events_ottawa.csv')
