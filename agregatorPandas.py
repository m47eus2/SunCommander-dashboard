import pandas as pd 
import os
import csv
from datetime import datetime, timedelta

def log(info):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{now}]: {info}")

#Calculating yesterday date
yesterday = datetime.now() - timedelta(days=1)
PATH = f"database/{yesterday.strftime('%Y-%m-%d')}-log.csv"

#Opening csv data from yesterday
data = pd.read_csv(PATH)

#Resampling data
data['time'] = pd.to_datetime(data['time'], format="%Y-%m-%d %H:%M:%S")
data.set_index("time", inplace=True)
data = data.resample("1Min").mean()
data = data.reset_index()
print(data)

#Opening agregated data csv
AGRPATH = "database/agrData.csv"
if not os.path.isfile(AGRPATH):
    with open(AGRPATH, 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(data.columns.tolist())
        log("Created new agrData.csv file")

data.to_csv(AGRPATH, index=False)