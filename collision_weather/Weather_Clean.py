import csv
import os
import pandas as pd
#clean the weather data, we need to assure that each useful record has at least one attribute about temperature
#the file is too big so we have chunksize 1000000 and then we use merege.py to link them
table = pd.read_csv("/home/kkyykk/Desktop/ontario_1_2.csv",chunksize=1000000,low_memory=False)
i=0
os.mkdir("/home/kkyykk/Desktop/ontario_1_2")
for data in table:
    #data=data.dropna(axis=0,thresh=14)
    #at least 7 attri to analyse
    data = data[data['Temp...C.'].notnull()]
    clean_data=data.loc[data['X.U.FEFF..Station.Name.'].str.contains('OTTAWA|TORONTO')]
    print(clean_data.head(5))
    if clean_data.empty:
        print("eeeeeempty df")
        continue
    clean_data.to_csv("/home/kkyykk/Desktop/ontario_1_2/ontario_1_2--"+str(i)+".csv")
    i=i+1
