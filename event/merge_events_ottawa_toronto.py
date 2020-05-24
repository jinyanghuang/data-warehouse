import pandas as pd

df_ottawa = pd.read_csv('events_ottawa.csv', index_col=0, dtype={'hour': str})

df_toronto = pd.read_csv('events_toronto.csv', index_col=0, dtype={'hour': str})

df_merged = df_ottawa.append(df_toronto, sort=False)
df_merged.to_csv('events_ottawa_toronto.csv', index=False, encoding='utf-8')