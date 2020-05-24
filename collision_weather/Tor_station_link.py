import pandas as pd
import math
df = pd.read_csv("/home/kkyykk/Desktop/data_science/Toronto_fi.csv",low_memory=False)
#print(df['X.U.FEFF..Station.Name.'].value_counts())
stationlist=[]
station_to = {'TORONTO BUTTONVILLE A':[43.86,-79.37],'TORONTO INTL A':[43.68,-79.63],'TORONTO CITY CENTRE':[43.63,-79.4],'TORONTO CITY':[43.67,-79.4],'PA TORONTO HYUNDAI':[43.7,-79.45]
,'PA TORONTO NORTH YORK MOTORS':[43.72,-79.47],'PA SCARBOROUGH TORONTO HUNT':[43.68,-79.27],'PA TORONTO INTERNATIONAL TRAP AND SKEET':[44.19,-79.66]}#OTTAWA CDA RCS ,OTTAWA INTL A
ll=['TORONTO BUTTONVILLE A','TORONTO INTL A','TORONTO CITY CENTRE','TORONTO CITY','PA TORONTO HYUNDAI','PA TORONTO NORTH YORK MOTORS','PA SCARBOROUGH TORONTO HUNT','PA TORONTO INTERNATIONAL TRAP AND SKEET']
weather_data=pd.read_csv("./total_Ontario_final.csv",low_memory=False)
for index in df.index:
    lat=df['LATITUDE'][index]#45....
    lon=df['LONGITUDE'][index]#-75...
    Year=df['Year'][index]
    Month=df['Month'][index]
    Day=df['Day'][index]
    Hour=df['Hour'][index]
    print(Hour)
    #print(weather_data['Time'])
    mi=[]
    for key,i in station_to.items():
        dis=((lat-i[0])**2+(lon-i[1])**2)**0.5
        mi.append(dis)
    for i in range(len(mi)):
        ind=mi.index(min(mi))
        name=ll[ind]#find the min one in mi list
        data=weather_data[(weather_data['X.U.FEFF..Station.Name.']==name)&(weather_data['Year']==Year)&(weather_data['Month']==Month)&(weather_data['Day']==Day)]#
        if data.empty:#empty??
            mi.pop(ind)
            if mi:
                print("")
            else:#no station fits the collision data, the mi list is empty
                finalname="NA"
                
        else:
            finalname=name
    stationlist.append(finalname)
df['station']=stationlist
df=df[df['Year']>2013]
df.to_csv("/home/kkyykk/Desktop/Toronto_final_improve.csv")

