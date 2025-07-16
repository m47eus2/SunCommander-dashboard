import csv
import os
import datetime
import random
from datetime import datetime
import time

PATH = "data.csv"

def log(now,prod,ra,rb,rc,b1,b2,energy):
    fileExists = os.path.isfile(PATH)
    with open(PATH, 'a', newline='') as file:
        writer = csv.writer(file)
        if not fileExists:
            writer.writerow(['time','prod','ra','rb','rc','b1','b2','energy'])
            print("First row created")
        writer.writerow([now,prod,ra,rb,rc,b1,b2,energy])
        print(f"Data logged -> {now}")


while(True):
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    log(now, random.randrange(1000),random.randrange(1000),random.randrange(1000),random.randrange(1000),random.randrange(1000),random.randrange(1000),random.randrange(1000))
    time.sleep(1)