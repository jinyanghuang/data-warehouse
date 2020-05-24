-- Roll up
-- determine the total number of fatalities in Ottawa during 2015
SELECT H.year, H.month, H.day, H.hour, count(*) AS fatalities
FROM accident_fact A,
     hour_dim H
WHERE A.hour_key = H.hour_key
  AND H.year = '2015'
  AND A.is_fatal = '1'
GROUP BY ROLLUP (H.year, H.month, H.day, H.hour);

-- Drill down
-- determine the total number of fatalities in Ottawa during 2015.
SELECT H.year, H.month, H.day, H.hour, count(*)
FROM accident_fact A,
     hour_dim H
WHERE A.hour_key = H.hour_key
  AND H.year = '2015'
  AND A.is_fatal = '1'
GROUP BY
  GROUPING SETS ((), (H.hour), (H.day, H.hour), (H.month, H.day, H.hour), (H.year, H.month, H.day, H.hour));

-- Slice
-- compare the number of accidents on Mondays, versus the number of accidents on Fridays
SELECT H.day_of_week, count(*)
FROM accident_fact A,
     hour_dim H
WHERE A.hour_key = H.hour_key
  AND (H.day_of_week = 1 OR H.day_of_week = 5)
GROUP BY GROUPING SETS ((H.day_of_week));

-- Dice
-- contrast the number of fatal accidents in Ottawa, during 2017, with the number of fatalities in Toronto, during 2014.
SELECT L.city, H.year, count(*) AS fatal_count
FROM accident_fact A,
     hour_dim H,
     location_dim L
WHERE A.hour_key = H.hour_key
  AND A.location_key = L.location_key
  AND ((H.year = '2017' AND L.city = 'Ottawa')
  OR (H.year = '2014' AND L.city = 'Toronto'))
  AND is_fatal = '1'
GROUP BY GROUPING SETS ((L.city, H.year));

-- Slice
-- contrast the total number of accidents during summer, with the number of fatalities during fall
SELECT CASE
         WHEN CAST(H.month AS INTEGER) BETWEEN 7 AND 9 THEN 'summer'
         WHEN CAST(H.month AS INTEGER) BETWEEN 10 AND 12 THEN 'fall'
         END
                                                            AS season,
       count(*)                                             AS accident_count,
       count(CASE WHEN is_fatal = '1' THEN 1 ELSE NULL END) AS fatal_count
FROM accident_fact A,
     hour_dim H
WHERE A.hour_key = H.hour_key
  AND CAST(H.month AS INTEGER) BETWEEN 7 AND 12
GROUP BY season;

-- Top N
-- determine the intersections with the most accidents over the four years.
-- The reason Toronto is not on the list is that it only reports fatal accidents
SELECT city, street1, street2, count(*) AS accident_count
FROM accident_fact A,
     location_dim L
WHERE A.location_key = L.location_key
GROUP BY street1, street2
ORDER BY accident_count DESC
LIMIT 1000;

-- Dice
-- determine the monthly trends in fatal accidents in Ottawa during the four years
SELECT H.year, H.month, count(*) AS fatal_count
FROM accident_fact A,
     hour_dim H,
     location_dim L
WHERE A.hour_key = H.hour_key
  AND A.location_key = L.location_key
  AND L.city = 'Ottawa'
  AND A.is_fatal = '1'
GROUP BY GROUPING SETS ((H.year, H.month))
ORDER BY H.year, CAST(H.month AS INTEGER);

-- Top N
-- The 3 months having the most accidents in Ottawa in 2015
SELECT H.month, count(*) AS count
FROM accident_fact A,
     hour_dim H,
     location_dim L
WHERE A.hour_key = H.hour_key
  AND A.location_key = L.location_key
  AND H.year = '2015'
  AND L.city = 'Ottawa'
GROUP BY H.month
ORDER BY count DESC
LIMIT 3;

-- Bottom N
-- The 3 months having the least accidents in Ottawa in 2015
SELECT H.month, count(*) AS count
FROM accident_fact A,
     hour_dim H,
     location_dim L
WHERE A.hour_key = H.hour_key
  AND A.location_key = L.location_key
  AND H.year = '2015'
  AND L.city = 'Ottawa'
GROUP BY H.month
ORDER BY count ASC
LIMIT 3;

