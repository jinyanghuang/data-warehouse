Staging scripts：
Before upload the data in the Postgresql Database, we firstly clean the weather and collision data 
by pandas using python. 

Cleaning Step:
1.Weather_Clean.py: 
  Clean the weather cvs files, the condition is each useful record has at least one 
attribute about temperature and the record's station_name should contain 'OTTAWA' or 'TORONTO'.
The file is too big so we have chunksize 1000000 and then we use merege.py to link them.

2.Weather_delete.py:
  Delete some of the data which are recorded before 2014.

3.Ottawa_date.py:
  split the Date attribute into Year, Month, Day.
For example, '2014/12/2'---->Year:'2014', Month:'12', Day:'2'

4.merge.py
  Merge the sub-weather data that were produced in Weather_Clean.py

5.Tor_light.py:
  In the weather data of Toronto, for the attribute 'Light', some of
the values have comma in it and the word after the comma is useless,
so we delete the word after the comma in this file.

After data cleaning, we also use python to link the nearest station name to
collision data.
Link Step:
1.Ottawa_Collision.py:
  In this file, we find the nearest station for each collision record. The condition
is that in this specific Year, Month, Day the nearest station should have weather record
so that we can link them. The nearest station is found through LATITUDE and LONGITUDE with
Euclidean distance.
  Also, we split the attribute 'Location' in Ottawa_Collision.csv to street1, street2 and road_name
For example, 
  1)MONTREAL RD btwn ELWOOD ST & BECKENHAM LANE ----> street1:ELWOOD ST, street2:BECKENHAM LANE, road_name:MONTREAL RD
  2)AVIATION PKWY @ OGILVIE RD----> street1:AVIATION PKWY, street2:OGILVIE RD, road_name:AVIATION PKWY

2.Tor_station_link.py:
  In this file, we link the nearest station name to each record. The condition is same to the Ottawa.

3.Calgary_Collision.py:
  In this file, we clean the Calgary_Collision.csv file and we also link the station for Clagary's collision data.
Mapping's condition is same to the Ottawa.
The attributes we clean in this file are:
  Date---->Year, Month, Day
  Intersection
  Loction---->street1, street2, road_name
