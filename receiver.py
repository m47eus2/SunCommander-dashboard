import serial
import time 
import os
import csv
import glob
import pandas as pd
from datetime import datetime 

class Data:
    def __init__(self):
        self.data = {
            'time':'0',
            'Irms0':'0',
            'Irms0-total':'0',
            'a':'0',
            'b':'0',
            'c':'0',
            'a-total':'0',
            'b-total':'0',
            'c-total':'0',
            'a-state':'0',
            'b-state':'0',
            'c-state':'0',
            'b0':'0',
            'b1':'0',
            'p':'0',
            'e':'0'
        }

        #Getting last values of receivers and production energy
        (self.receiverEnergy, self.productionEnergy) = self.getLastEnergyValues()

        self.powerKeys = ['Irms0','a','b','c','a-total','b-total','c-total']
        self.stateKeys = ['a-state','b-state','c-state','b0','b1']
        self.timer = 0

    #Getting line from serial, splitting it to key and value, changing current values to power and writing it to dictionary
    def collectData(self, line):
        line = line.split(':')
        key = line[0][1:]

        if key in self.powerKeys:
            self.data[key] = self.currentToPower(line[1])
        if key in self.stateKeys:
            try:
                self.data[key] = float(line[1])
            except:
                self.data[key] = 0.0
        if key == 'b1':
            #When last value comes filling dict and writing it to csv
            self.writeToCsv()

    def writeToCsv(self):
        PATH = f"database/{datetime.now().strftime('%Y-%m-%d')}-log.csv"
        fileExists = os.path.isfile(PATH)
        with open(PATH, 'a', newline='') as file:
            writer = csv.writer(file)
            if not fileExists:
                writer.writerow(self.data.keys())
            #Filling dictionary last values -> time, modyfing Irms0, receivers total power, calculating energies, 
            self.fillRow()
            #Writing dictionary to csv
            writer.writerow(self.data.values())
            #Reseting timer for calculating energy
            self.timer = time.perf_counter()
            self.resetValues()

    def fillRow(self):
        self.data['time'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.data['Irms0'] = float(self.data['Irms0'])*3.0
        receiversPower = self.calcReceiversPower()
        self.receiverEnergy += self.calcEnergy(receiversPower)
        self.productionEnergy += self.calcEnergy(float(self.data['Irms0']))
        self.data['Irms0-total'] = self.productionEnergy
        self.data['p'] = receiversPower
        self.data['e'] = self.receiverEnergy

    def calcReceiversPower(self):
        power = 0.0
        if bool(self.data['a-state']):
            power += float(self.data['a-total'])
        if bool(self.data['b-state']):
            power += float(self.data['b-total'])
        if bool(self.data['c-state']):
            power += float(self.data['c-total'])
        return power
    
    def calcEnergy(self, power):
        if self.timer:
            currentTime = time.perf_counter()
            energyTime = (currentTime - self.timer)/3600
            return power*energyTime
        else:
            return 0.0

    def currentToPower(self, current):
        try:
            power = (float(current)*230.0)/1000.0
        except:
            power = 0.0
        return power
    
    def getLastEnergyValues(self):
        linesToTry = 5
        files = glob.glob("database/*-log.csv")
        if files:
            PATH = sorted(files)[-1]
            csvFile=pd.read_csv(PATH)
            csvFile=csvFile.tail(linesToTry)
            for i in range(linesToTry-1, -1, -1):
                try:
                    self.log(f"Trying to read latest values from line {i}")
                    return (float(csvFile['e'].values[i]), float(csvFile['Irms0-total'].values[i]))
                except:
                    self.log(f"Cannot read latest values from line {i}")
                    continue
            self.log("Connot read latest values, setting them to 0")
            return (0.0 , 0.0)
        else:
            return (0.0, 0.0)

    def resetValues(self):
        for key in self.data.keys():
            self.data[key] = '0'
    
    def log(self,info):
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{now}]: {info}")

class App():
    def __init__(self):
        self.port = "/dev/ttyUSB0"
        #self.port = "/dev/ttyACM0" #for oryginal uno
        self.baudrate = 115200
        self.connection = False
        self.data = Data()

        self.run()

    def run(self):
        while True:
            try:
                self.log(f"Trying to connect with {self.port}")
                self.serialPort = serial.Serial(self.port, self.baudrate, timeout=3)
                self.log(f"Connected with {self.port}")
                time.sleep(4)

                try:
                    self.receivingData()
                except Exception as e:
                    self.log(f"Error while receiving data -> {e}")
                finally:
                    self.serialPort.close()
                
            except Exception as e:
                self.log(f"Cannot connect with {self.port} -> {e}")
                self.serialPort.close()
                time.sleep(5)

    def receivingData(self):
        while True:
            if self.serialPort.in_waiting:
                self.sendTimeInfo()
                line = self.serialPort.readline().decode("utf-8").rstrip()
                print(line)
                self.data.collectData(line)
            else:
                time.sleep(0.01)

    def sendTimeInfo(self):
        hour = datetime.now().strftime("%H")
        info = 1 if 12 <= int(hour) <= 16 else 0
        self.serialPort.write(f"{info}\n".encode())

    def log(self,info):
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{now}]: {info}")

app = App()