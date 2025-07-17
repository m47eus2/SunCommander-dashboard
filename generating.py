import csv
import os
import random
from datetime import datetime
import time
import pandas as pd

PATH = "data.csv"

def getCEnergyValue():
    if os.path.isfile(PATH):
        data = pd.read_csv(PATH)
        data = data.tail(1)
        return int(data['cEnergy'].values[0])
    else:
        return 0


def log(now,prod,ra,rb,rc,sa,sb,sc,b1,b2,energy):
    fileExists = os.path.isfile(PATH)
    with open(PATH, 'a', newline='') as file:
        writer = csv.writer(file)
        if not fileExists:
            writer.writerow(['time','prod','ra','rb','rc','sa','sb','sc','b1','b2','energy','cEnergy'])
            print("First row created")
        cEnergy["value"] += energy
        writer.writerow([now,prod,ra,rb,rc,sa,sb,sc,b1,b2,energy,cEnergy["value"]])
        print(f"Data logged -> {now}")

cEnergy = {"value":getCEnergyValue()}

while(True):
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    log(now, random.randrange(1000),random.randrange(1000),random.randrange(1000),random.randrange(1000),random.randrange(2),random.randrange(2), random.randrange(2),random.randrange(1000),random.randrange(1000),random.randrange(1000))
    time.sleep(1)