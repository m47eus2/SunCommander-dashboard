import csv
import os
import random
from datetime import datetime
import time
import pandas as pd
import glob

def getCEnergyValue():
    files = glob.glob("database/*-log.csv")
    if files:
        PATH = sorted(files)[-1]
        data = pd.read_csv(PATH)
        data = data.tail(1)
        return int(data['cEnergy'].values[0])
    else:
        return 0


def log(now,prod,ra,rb,rc,sa,sb,sc,b1,b2,energy):
    date = datetime.now().strftime("%Y-%m-%d")
    PATH = f"database/{date}-log.csv"
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

sa = 0
sb = 0
sc = 0

while(True):
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    rand=random.randrange(10)
    if rand > 8: sa=random.randrange(2)
    rand=random.randrange(10)
    if rand > 8: sb=random.randrange(2)
    rand=random.randrange(10)
    if rand > 8: sc=random.randrange(2)
    log(now, random.randrange(1000),random.randrange(1000),random.randrange(1000),random.randrange(1000), sa, sb, sc ,random.randrange(1000),random.randrange(1000),random.randrange(1000))
    time.sleep(1)