import pandas as pd
#clean the data to get the collisions after 2014
#clean the unnecessary attribute Unnamed:0.1 and Unnamed:0.1.1
dt = pd.read_csv("/home/kkyykk/Desktop/total_calgary.csv",low_memory=False)
print(dt.columns.values)
dt.drop(['Unnamed: 0.1','Unnamed: 0','Unnamed: 0.1.1'],axis=1,inplace=True)
dt=dt[dt["Year"]>2013]
print(dt.columns.values)
dt.to_csv("/home/kkyykk/Desktop/Ontario_Weather_temp/total_Calgary_final.csv")
