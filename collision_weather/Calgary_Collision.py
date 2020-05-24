import pandas as pd
import math
df = pd.read_csv("/home/kkyykk/Desktop/data_science/Calgary_final.csv",low_memory=False)
#print(df['X.U.FEFF..Station.Name.'].value_counts())
station_ow = {'CALGARY INTL A':[51.12,-114.01],"CALGARY INT'L CS":[51.11,-114],"CALGARY SPRINGBANK A":[51.11,-114.37]}#OTTAWA CDA RCS ,OTTAWA INTL A
ll=['CALGARY INTL A',"CALGARY INT'L CS","CALGARY SPRINGBANK A"]
stationlist=[]
Yearlist=[]
Monthlist=[]
Daylist=[]


weather_data=pd.read_csv("./total_Calgary_final.csv",low_memory=False)

for index in df.index:
    lat=df['LATITUDE'][index]#45....
    lon=df['LONGITUDE'][index]#-75...
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
                print("no")
            else:#no station fits the collision data, the mi list is empty
                finalname="NA"
                
        else:
            finalname=name
    stationlist.append(finalname)
df['station']=stationlist


#df['Date'].apply('str')
for i in df.index:
    date = df['DATE'][i]
    Yearlist.append(int(date[0:4]))
    MonthDay=date[5:]
    ind=MonthDay.index('/')
    Monthlist.append(int(MonthDay[0:ind]))
    Daylist.append(int(MonthDay[ind+1:]))
df['Hour']=12
road_namelist=[]
street1list=[]
street2list=[]
intersectionlist=[]
for i in df.index:
    loction = df['COLLISION_LOCATION'][i]
    print(loction)
    if loction.find("&")!=-1:
        ind=loction.index("&")
        street1=loction[0:ind-1]
        street1list.append(street1)
        road_name=street1
        road_namelist.append(road_name)
        street2=loction[ind+1:]
        street2list.append(street2)
        intersectionlist.append("AT Intersection")
    else:
        street1list.append("")
        street2list.append("")
        road_namelist.append(loction)
        intersectionlist.append("NOT Intersection")

df['Road_surface']=""
df['Traffic_Control']=""
df['light']=""
df['Collision_Classification']=""
df['Visibility']=""
df['Impact_type']=""
df['Intersection']=intersectionlist
df['Month']=Monthlist
df['Year']=Yearlist
df['Day']=Daylist
df['Road_name']=road_namelist
df['street1']=street1list
df['street2']=street2list
df=df[df["Year"]>2013]
df.to_csv("/home/kkyykk/Desktop/Calgary_final_improve.csv")
