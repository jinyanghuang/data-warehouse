import pandas as pd
import math
df = pd.read_csv("./Ottawa_fin.csv",low_memory=False)
#data = pd.read_csv("/home/kkyykk/Desktop/14.csv",low_memory=False)
#print(data['X.U.FEFF..Station.Name.'].value_counts())
station_ow = {'OTTAWA CDA RCS':[45.38,-75.72],'OTTAWA INTL A':[45.32,-75.67]}#OTTAWA CDA RCS ,OTTAWA INTL A
ll=['OTTAWA CDA RCS','OTTAWA INTL A']
stationlist=[]
road_namelist=[]
street1list=[]
street2list=[]
interlist=[]
name=""
finalname=""
'''improve'''
weather_data=pd.read_csv("./total_Ontario_final.csv",low_memory=False)

for index in df.index:
    lat=df['lat'][index]#45....
    lon=df['lon'][index]#-75...
    Year=df['Year'][index]
    Month=df['Month'][index]
    Day=df['Day'][index]
    Hour=df['Hour'][index]
    print(Hour)
    print(weather_data['Time'])
    mi=[]
    for key,i in station_ow.items():
        dis=((lat-i[0])**2+(lon-i[1])**2)**0.5
        mi.append(dis)
    for i in range(len(mi)):
        ind=mi.index(min(mi))
        name=ll[ind]#find the min one in mi list
        data=weather_data[(weather_data['X.U.FEFF..Station.Name.']==name)&(weather_data['Year']==Year)&(weather_data['Month']==Month)&(weather_data['Day']==Day)]#&(weather_data['Time']==Hour)
        if data.empty:#empty??
            mi.pop(ind)
            if mi:
                print("")
            else:#no station fits the collision data, the mi list is empty
                finalname="NA"
                break
        else:
            finalname=name
    stationlist.append(finalname)
df['station']=stationlist
'''above is the map of the station'''

'''now we split the Location attribute into street1,street2 and road_name'''
for i in df.index:
    loction = df['Location'][i]
    print(loction)
    if loction.find("@")!=-1:
        ind=loction.index("@")
        street1=loction[0:ind-1]
        street1list.append(street1)
        road_name=street1
        road_namelist.append(road_name)
        street2=loction[ind+1:]
        street2list.append(street2)
    elif loction.find("btwn")!=-1:
        ind=loction.index("btwn")
        if loction.find("&")!=-1:
            ind1=loction.index("&")
            road_name=loction[0:ind-1]
            road_namelist.append(road_name)
            street1=loction[ind+5:ind1-1]
            street1list.append(street1)
            street2=loction[ind1+1:]
            street2list.append(street2)
        else:
            road_name=loction[0:ind-1]
            road_namelist.append(road_name)
            street1=loction[ind+5:]
            street1list.append(street1)
            street2list.append("")
    else:
        street1list.append("")
        street2list.append("")
        road_namelist.append(loction)
    #Now we handle the intersection
    inter = df['Collision_Location'][i]
    if inter == 'At intersection' or inter == 'Intersection related' :
        interlist.append(1)
    else:
        interlist.append(0)
df['road_name']=road_namelist
df['street1']=street1list
df['street2']=street2list
df['neighbour']=""

df.to_csv("/home/kkyykk/Desktop/Ottawa_final_improve.csv")
