import math
import pandas as pd
'''remove unnecessary word: 'artificale'
in light attribute'''
lightlist=[]
df = pd.read_csv("/home/kkyykk/Desktop/Toronto_fin.csv",low_memory=False)
for index in df.index:
    light=df['LIGHT'][index]#45....
    if light.find(',')!=-1:
        ind = light.index(',')
        new=light[0:ind]
        lightlist.append(new)
    else:
        lightlist.append(light)
df['LIGHT']=lightlist
df.to_csv("/home/kkyykk/Desktop/Toronto_fi.csv")
