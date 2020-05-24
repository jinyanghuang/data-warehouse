import os
import pandas as pd
dirs=os.listdir("/home/kkyykk/Desktop/Ontario_Weather_temp")
for ind,fil in enumerate(dirs):
    dt = pd.read_csv("/home/kkyykk/Desktop/Ontario_Weather_temp/"+fil,low_memory=False)
    if ind == 0:
        dv = dt
        continue
    dv = dv.append(dt)
dv.to_csv("/home/kkyykk/Desktop/Ontario_Weather_temp/.csv")
