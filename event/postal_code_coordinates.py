import psycopg2

import pandas as pd

import conf

filter_sql = '''
SELECT postal_code
FROM event_dim
WHERE postal_code SIMILAR TO '[A-Z]\d[A-Z]\s?\d[A-Z]\d'
  AND latitude = 'NA'
  AND longitude = 'NA'
'''

update_sql = '''
UPDATE event_dim
SET latitude = %s,
    longitude = %s
WHERE (postal_code = %s OR postal_code = %s) 
  AND latitude = 'NA'
  AND longitude = 'NA'
'''


df_pc = pd.read_csv('Canadian Postal Codes.csv', usecols=['PostalCode', 'Latitude', 'Longitude'])

with psycopg2.connect(host='web0.eecs.uottawa.ca', port=15432, dbname='group_9', user='xchen200', password=conf.password) as conn:
    with conn.cursor() as cur:
        cur.execute(filter_sql)
        records = cur.fetchall()

    with conn.cursor() as cur:
        for record in records:
            pc_no_space = record[0].strip().replace(' ', '')
            coords: pd.DataFrame = df_pc.loc[df_pc['PostalCode'] == pc_no_space]
            if not coords.empty:
                # Two format possibilities in DB for postal code: w/ or w/o space
                pc_with_space = f'{pc_no_space[:3]} {pc_no_space[-3:]}'
                tup = (*tuple(coords.iloc[0])[1:], pc_no_space, pc_with_space)
                cur.execute(update_sql, tup)
                print('Updated:', tuple(coords.iloc[0]))