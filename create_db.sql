-- Create weather flat table
CREATE TABLE weather_flat
(
  Year             varchar,
  Month            varchar,
  Day              varchar,
  Time             varchar,
  Temp_C           varchar,
  Dew_Point_Temp_C varchar,
  Rel_Hum          varchar,
  Wind_Dir_10sDeg  varchar,
  Wind_spd_km      varchar,
  Visibility_km    varchar,
  Stn_Press_kPa    varchar,
  Hmdx             varchar,
  Wind_Chill       varchar,
  Weather          varchar,
  Station_names    varchar,
  Province         varchar
);

-- CREATE station reference table
CREATE TABLE station_reference_table
(
  Station_name varchar,
  Latitude     varchar,
  Longitude    varchar
);


-- Extract hour dimension table from weather_flat table
CREATE TABLE hour_dim AS
SELECT DISTINCT year, month, day, "hour"
FROM weather_flat;
-- Add surrogate key to hour_dim
ALTER TABLE hour_dim
  ADD COLUMN hour_key SERIAL PRIMARY KEY;

-- Add a hour_key column to weather_flat table
ALTER TABLE weather_flat
  ADD COLUMN hour_key varchar;

-- Map hour_key
update weather_flat
set hour_key= hour_dim.hour_key
from hour_dim
where weather_flat.year = hour_dim.year
  AND weather_flat.month = hour_dim.month
  AND weather_flat.day = hour_dim.day
  AND weather_flat.hour = hour_dim.hour;

-- Extract weather dimension table from weather_flat table
CREATE TABLE weather_dim as
SELECT DISTINCT temp_c,
                dew_point_temp_c,
                rel_hum,
                wind_dir_10sdeg,
                wind_spd_km,
                visibility_km,
                stn_press_kpa,
                hmdx,
                wind_chill,
                weather,
                station_names
FROM weather_flat;

-- Add surrogate key to weather_dim
ALTER TABLE weather_dim
  ADD COLUMN weather_key SERIAL PRIMARY KEY;

-- Add a weather_key column to weather_flat table
ALTER TABLE weather_flat
  ADD COLUMN weather_key varchar;

-- Map weather key
update weather_flat
set weather_key= weather_dim.weather_key
from weather_dim
where weather_flat.temp_c = weather_dim.temp_c
  AND weather_flat.dew_point_temp_c = weather_dim.dew_point_temp_c
  AND weather_flat.rel_hum = weather_dim.rel_hum
  AND weather_flat.wind_dir_10sdeg = weather_dim.wind_dir_10sdeg
  AND weather_flat.wind_spd_km = weather_dim.wind_spd_km
  AND weather_flat.visibility_km = weather_dim.visibility_km
  AND weather_flat.stn_press_kpa = weather_dim.stn_press_kpa
  AND weather_flat.hmdx = weather_dim.hmdx
  AND weather_flat.wind_chill = weather_dim.wind_chill
  AND weather_flat.weather = weather_dim.weather
  AND weather_flat.station_names = weather_dim.station_names;

-- Add latitude and longitude to weather dimension table
UPDATE weather_dim
set longitude = station_reference_table.longitude
FROM station_reference_table
where weather_dim.station_names = station_reference_table.station_name;

-- Create collision flat table
CREATE TABLE collision_flat
(
  city            varchar,
  road_name       varchar,
  street1         varchar,
  street2         varchar,
  neighbour       varchar,
  latitude        varchar,
  longitude       varchar,
  year            varchar,
  month           varchar,
  day             varchar,
  hour            varchar,
  road_surface    varchar,
  traffic_control varchar,
  intersection    varchar,
  light           varchar,
  is_fatal        varchar,
  impact_type     varchar,
  visibility      varchar,
  station_name    varchar
);

-- Add surrogate key to collision_flat
ALTER TABLE collision_flat
  ADD COLUMN accident_key SERIAL PRIMARY KEY;

-- Extract location dimension table from collision_flat
CREATE TABLE location_dim as
SELECT DISTINCT city, road_name, street1, street2, neighbour, latitude, longitude
FROM collision_flat;

-- Add surrogate key to location_dim
ALTER TABLE location_dim
  ADD COLUMN location_key SERIAL PRIMARY KEY;

-- Add a location_key, weather_key, hour_key column to collision_flat table
ALTER TABLE collision_flat
  ADD COLUMN location_key varcher;
ALTER TABLE collision_flat
  ADD COLUMN weather_key varcher;
ALTER TABLE collision_flat
  ADD COLUMN hour_key varcher;

-- Map weather and hour dimension
update collision_flat
set weather_key = weather_flat.weather_key,
    hour_key=weather_flat.hour_key
from weather_flat
where weather_flat.year = collision_flat.year
  AND weather_flat.month = collision_flat.month
  AND weather_flat.day = collision_flat.day
  AND weather_flat.hour = collision_flat.hour
  AND weather_flat.station_names = collision_flat.station_name;

-- Map location
update collision_flat
set location_key = location_dim.location_key
from location_dim
where collision_flat.city = location_dim.city
  and collision_flat.road_name = location_dim.road_name
  and collision_flat.street1 = location_dim.street1
  and collision_flat.street2 = location_dim.street2
  and collision_flat.neighbour = location_dim.neighbour
  and collision_flat.latitude = location_dim.latitude
  and collision_flat.longitude = location_dim.longitude

-- Create fact table
CREATE TABLE accident_fact as
SELECT DISTINCT hour_key, weather_key, accident_key, location_key, is_fatal, intersection
FROM collision_flat;

-- Rename collision_flat to accident_dim
ALTER TABLE collision_flat
  RENAME TO accident_dim;

ALTER TABLE accident_fact
  ADD CONSTRAINT constraint_fk
    FOREIGN KEY (accident_key)
      REFERENCES accident_dim (accident_key)
      ON DELETE RESTRICT
      ON UPDATE RESTRICT;

-- Create event dim
create table event_dim
(
  city         varchar,
  year         varchar,
  month        varchar,
  day          varchar,
  hour         varchar,
  event_name   varchar,
  city_sector  varchar,
  address      varchar,
  intersection varchar,
  postal_code  varchar,
  latitude     varchar,
  longitude    varchar
);

ALTER TABLE event_dim
  ADD COLUMN event_key SERIAL PRIMARY KEY;

ALTER TABLE accident_fact
  ADD COLUMN event_key int;

update accident_fact
set event_key = event_dim.event_key
from event_dim,
     hour_dim,
     location_dim
where accident_fact.hour_key = hour_dim.hour_key
  and location_dim.location_key = accident_fact.location_key
  and event_dim.city = location_dim.city
  and event_dim.year = hour_dim.year
  and event_dim.month = hour_dim.month
  and event_dim.day = hour_dim.day
  and event_dim.hour = hour_dim.hour
