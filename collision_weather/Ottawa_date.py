import csv
import os
import pandas as pd
#split the Date attribute into Year, Month, Day
df = pd.read_csv("/home/kkyykk/Desktop/Ottawa.csv")
#df['Date'].apply('str')
df['Year']=df['Date'].str.slice(0,4)
df['Month']=df['Date'].str.slice(5,7)
df['Day']=df['Date'].str.slice(8,10)
df.to_csv("/home/kkyykk/Desktop/Ottawa_clean.csv")
