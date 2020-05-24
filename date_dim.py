from datetime import date
import holidays
import psycopg2

import conf

on_holidays = holidays.CountryHoliday('CA', prov='ON')
ab_holidays = holidays.CountryHoliday('CA', prov='AB')

with psycopg2.connect(host='web0.eecs.uottawa.ca', port=15432, dbname='group_9', user='xchen200', password=conf.password) as conn:
    with conn.cursor() as cur:
        cur.execute('SELECT DISTINCT "year", "month", "day" '
                    'FROM hour_dim')
        for record in cur.fetchall():
            date_tup = date(*map(int, record))
            cur.execute('UPDATE hour_dim '
                        'SET weekend = %s, '
                        '    holiday = %s, '
                        '    holiday_name = %s, '
                        '    day_of_week = %s '
                        'WHERE "year" = %s AND'
                        '      "month" = %s AND'
                        '      "day" = %s',
                        (date_tup.weekday() > 4,
                         date_tup in on_holidays or date_tup in ab_holidays,
                         on_holidays.get(date_tup) if date_tup in on_holidays else ab_holidays.get(date_tup),
                         date_tup.weekday() + 1,
                         str(date_tup.year),
                         str(date_tup.month),
                         str(date_tup.day)))
