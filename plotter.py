from bokeh.layouts import column, row
from bokeh.models import ColumnDataSource, Select, TextInput
from bokeh.plotting import figure, curdoc
import pandas as pd
from datetime import datetime, timedelta
import os

class Graph():
    def __init__(self, title, colors, height, yLabel,csvColumns):

        self.sources = []
        for column in csvColumns:
            self.sources.append(ColumnDataSource(data=dict(x=[],y=[])))

        self.figure = figure(title=title,x_axis_type="datetime", y_axis_label=yLabel, height=height)

        for i in range(len(csvColumns)):
            self.figure.line(x='x', y='y', source=self.sources[i], color=colors[i], line_width=2)

        self.figure.sizing_mode = "stretch_width"
        self.csvColumns = csvColumns
    
    def update(self, data):
        for i in range(len(self.csvColumns)):
            self.sources[i].data = dict(x=data["time"], y=data[self.csvColumns[i]])

selectedTime = {
    "value":5,
    "type":0
    }

#Graphs
graphs = []

graphs.append(Graph("Produkcja", ["limegreen"], 400, "kW", ["Irms0"]))
graphs.append(Graph("Produkcja", ["limegreen"], 400, "kWh", ["Irms0-total"]))

graphs.append(Graph("Moc", ["dodgerblue"], 400, "kW", ["p"]))
graphs.append(Graph("Energia", ["dodgerblue"], 400, "kWh", ["e"]))

graphs.append(Graph("Hala 1", ["cornflowerblue","tomato"], 400, "kW", ["a","a-total"]))
graphs.append(Graph("Hala 2", ["cornflowerblue","tomato"], 400, "kW", ["b","b-total"]))
graphs.append(Graph("Social", ["cornflowerblue","tomato"], 400, "kW", ["c","c-total"]))

graphs.append(Graph("Hala 1", ["steelblue"], 150, "", ["a-state"]))
graphs.append(Graph("Hala 2", ["steelblue"], 150, "", ["b-state"]))
graphs.append(Graph("Social", ["steelblue"], 150, "", ["c-state"]))

graphs.append(Graph("Boiler 1", ["lightseagreen"], 400, "", ["b0"]))
graphs.append(Graph("Boiler 2", ["lightseagreen"], 400, "", ["b1"]))

# Recent timespan selector 
selector = Select(title="Typ", value=0, options=[
    ('0','Minuty'),
    ('1','Godziny'),
    ('2','Dni'),
    ('3','Tygodnie'),
    ('4','Miesiące'),
    ('5','Lata')
])

def selectorUpdate(attr,old,new):
    selectedTime['type'] = int(new)

selector.on_change('value',selectorUpdate)

# Text input
textInput = TextInput(title="Wartość", value='10')

def textInputUpdate(attr,old,new):
    try:
        selectedTime["value"] = int(new)
    except:
        pass

textInput.on_change('value',textInputUpdate)

def update():
    #Reading recentData and agregatedData when it exists
    date = datetime.now().strftime("%Y-%m-%d")
    recentDataPATH = f"database/{date}-log.csv"
    agregatedDataPATH = "database/agrData.csv"

    recentData = pd.read_csv(recentDataPATH)
    if selectedTime["type"] > 0:
        recentData['time'] = pd.to_datetime(recentData['time'], format="%Y-%m-%d %H:%M:%S")
        recentData.set_index('time', inplace=True)
        recentData = recentData.resample("1Min").mean()
        recentData = recentData.reset_index()

    if (os.path.isfile(agregatedDataPATH)==1) & (selectedTime["type"]>1):
        agregatedData = pd.read_csv(agregatedDataPATH)
        data = pd.concat([agregatedData, recentData], ignore_index=True)
    else:
        data = recentData

    #Formating time collumn as datetime
    data['time'] = pd.to_datetime(data['time'], format="%Y-%m-%d %H:%M:%S")

    #Calculating cuttof date base on selected timespan
    if selectedTime['type'] == 0: tDelta = timedelta(minutes = selectedTime['value'])
    elif selectedTime['type'] == 1: tDelta = timedelta(hours = selectedTime['value'])
    elif selectedTime['type'] == 2: tDelta = timedelta(days = selectedTime['value'])
    elif selectedTime['type'] == 3: tDelta = timedelta(weeks = selectedTime['value'])
    elif selectedTime['type'] == 4: tDelta = timedelta(days = selectedTime['value']*31)
    elif selectedTime['type'] == 5: tDelta = timedelta(days = selectedTime['value']*365)

    cuttofDate = datetime.now() - tDelta

    #Filtering data with cuttof date
    data = data[data['time'] >= cuttofDate]

    for graph in graphs:
        graph.update(data)

#Graphs layout
layout = column(row(graphs[0].figure, graphs[1].figure, sizing_mode="stretch_width"),
                row(graphs[2].figure, graphs[3].figure, sizing_mode="stretch_width"),
                row(graphs[4].figure, graphs[5].figure, graphs[6].figure, sizing_mode="stretch_width"),
                row(graphs[7].figure, graphs[8].figure, graphs[9].figure, sizing_mode="stretch_width"),
                row(graphs[10].figure, graphs[11].figure, sizing_mode="stretch_width"),
                row(selector, textInput), 
                sizing_mode="stretch_width")

#Creating webpage and calling update function
curdoc().add_root(layout)
curdoc().add_periodic_callback(update, 1000)

#run with -> bokeh serve --show plotter.py