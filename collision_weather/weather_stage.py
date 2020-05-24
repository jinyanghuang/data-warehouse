import pandas as pd
from pandas import ExcelWriter
from pandas import ExcelFile

df = pd.read_excel('Ottawacollisionsfinal.xls', sheetname = '2015_all_records')

print(df.columns)


lightList=[]
roadSurfaceList=[]
trafficControlList=[]
collisionLocList=[]
collisionClassificationList=[]
impactTypeList=[]
visibilityList=[]
location = df['Location']
lat = df['lat']
lon = df['lon']
date = df['Date']
time = df['Time']
for i in df.index:
    roadSurface=df['Road_Surface'][i]
    if pd.isnull(roadSurface):
        roadSurfaceList.append("null")
    else:
        editedRoadSurface=roadSurface[5:]
        roadSurfaceList.append(editedRoadSurface)

    trafficControl=df['Traffic_Control'][i]
    if pd.isnull(trafficControl):
        trafficControlList.append("null")
    else:
        editedTraffic=trafficControl[5:]
        trafficControlList.append(editedTraffic)
    
    collisionLoc=df['Collision_Location'][i]
    if pd.isnull(collisionLoc):
        collisionLocList.append("null")
    else:
        editedColLoc=collisionLoc[5:]
        collisionLocList.append(editedColLoc)

    light=df['Light'][i]
    if pd.isnull(light):
        lightList.append("null")
    else:
        editedLight=light[5:]
        lightList.append(editedLight)

    collClass=df['Collision_Classification'][i]
    if pd.isnull(collClass):
        collisionClassificationList.append("null")
    else:
        editedColClass=collClass[5:]
        collisionClassificationList.append(editedColClass)
    
    impactType=df['Impact_type'][i]
    if pd.isnull(impactType):
        impactTypeList.append("null")
    else:
        editedImpactType=impactType[5:]
        impactTypeList.append(editedImpactType)

    visibility=df['Visibility'][i]
    if pd.isnull(visibility):
        visibilityList.append("null")
    else:
        editedVis=visibility[5:]
        visibilityList.append(editedVis)

dh = pd.DataFrame({'Location':location,
    'lat':lat,
    'lon':lon,
    'Date':date,
    'Time':time,
    'Road_Surface':roadSurfaceList,
    'Traffic_Control':trafficControlList,
    'Collision_Location':collisionLocList,
    'light':lightList,
    'Collision_Classification':collisionClassificationList,
    'Impact_type':impactTypeList,
    'Visibility':visibilityList
    })

writer = ExcelWriter('ottawa_dataCleaning.xlsx')
dh.to_excel(writer,'Sheet1',index=False)
writer.save()
