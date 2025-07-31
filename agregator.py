import pandas as pd
import csv
import os
from datetime import datetime, timedelta

def log(info):
    with open("logs/agregator.log", 'a') as file:
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        file.write(f"[{now}]: {info}\n")

yesterday = datetime.now() - timedelta(days=1)
PATH = f"database/{yesterday.strftime('%Y-%m-%d')}-log.csv"

data = pd.read_csv(PATH)
data['time'] = pd.to_datetime(data['time'], format="%Y-%m-%d %H:%M:%S")

avrRows = []

for hour in range(24):
    hourData = data[data['time'].dt.hour == hour]
    avrs = []
    avrs.append(f"{yesterday.strftime('%Y-%m-%d')} {hour:02d}:00:00")
    columns = data.columns.tolist()
    for colnum in range(1, len(columns)):
        avr = hourData[columns[colnum]].mean()
        avrs.append(avr if not pd.isnull(avr) else 0)
    avrRows.append(avrs)

AGRPATH = "database/agrData.csv"

fileExists = os.path.isfile(AGRPATH)
with open(AGRPATH, 'a', newline='') as file:
    writer = csv.writer(file)
    if not fileExists:
        writer.writerow(data.columns.tolist())
        log("Created new agrData.csv file")
    writer.writerows(avrRows)
    log(f"Agregated data from {PATH}")