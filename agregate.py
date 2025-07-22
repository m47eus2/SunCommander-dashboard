import pandas as pd
import csv
import os
from datetime import datetime, timedelta

yesterday = datetime.now() - timedelta(days=1)
PATH = f"database/{yesterday.strftime('%Y-%m-%d')}-log.csv"

data = pd.read_csv(PATH)
data['time'] = pd.to_datetime(data['time'], format="%Y-%m-%d %H:%M:%S")

avrRows = []

for i in range(24):
    hourData = data[data['time'].dt.hour == i]
    avr = []
    avr.append(f"{yesterday.strftime('%Y-%m-%d')} {i:02d}:00:00")
    columns = data.columns.tolist()
    for colnum in range(1, len(columns)):
        avr.append(hourData[columns[colnum]].mean())
    avrRows.append(avr)

AGRPATH = "agrData.csv"

fileExists = os.path.isfile(AGRPATH)
with open(AGRPATH, 'a', newline='') as file:
    writer = csv.writer(file)
    if not fileExists:
        writer.writerow(data.columns.tolist())
    writer.writerows(avrRows)