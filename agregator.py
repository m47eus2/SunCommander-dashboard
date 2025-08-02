import pandas as pd
import csv
import os
from datetime import datetime, timedelta

def log(info):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{now}]: {info}")

#Calculating yesterday date
yesterday = datetime.now() - timedelta(days=1)
PATH = f"database/{yesterday.strftime('%Y-%m-%d')}-log.csv"

#Opening csv data from yesterday
data = pd.read_csv(PATH)
data['time'] = pd.to_datetime(data['time'], format="%Y-%m-%d %H:%M:%S")

#Caltulating avarage of each value in each hour
avrRows = []
for hour in range(24):
    #Filtering data from one hour
    hourData = data[data['time'].dt.hour == hour]
    avrs = []
    #Adding datetime information to row
    avrs.append(f"{yesterday.strftime('%Y-%m-%d')} {hour:02d}:00:00")
    columns = data.columns.tolist()
    #Caltulating avarage of all values in specific hour
    for colnum in range(1, len(columns)):
        avr = hourData[columns[colnum]].mean()
        avrs.append(avr if not pd.isnull(avr) else 0)
    #Adding created row to rows list
    avrRows.append(avrs)

#Opening agregated data csv
AGRPATH = "database/agrData.csv"
fileExists = os.path.isfile(AGRPATH)
with open(AGRPATH, 'a', newline='') as file:
    writer = csv.writer(file)
    if not fileExists:
        writer.writerow(data.columns.tolist())
        log("Created new agrData.csv file")
    writer.writerows(avrRows)
    log(f"Agregated data from {PATH}")