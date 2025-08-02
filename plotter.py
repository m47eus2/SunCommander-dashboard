from bokeh.layouts import column, row
from bokeh.models import ColumnDataSource, Select
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

selectedTime = {"value":5}

#Graphs
graphs = []

graphs.append(Graph("Produkcja", ["limegreen"], 400, "kW", ["Irms0"]))
graphs.append(Graph("Produkcja", ["limegreen"], 400, "kWh", ["Irms0-total"]))


graphs.append(Graph("Moc", ["dodgerblue"], 400, "kW", ["p"]))
graphs.append(Graph("Energia", ["dodgerblue"], 400, "kWh", ["e"]))

graphs.append(Graph("Pobór odbiornik A", ["cornflowerblue","tomato"], 400, "kW", ["a","a-total"]))
graphs.append(Graph("Pobór odbiornik B", ["cornflowerblue","tomato"], 400, "kW", ["b","b-total"]))
graphs.append(Graph("Pobór odbiornik C", ["cornflowerblue","tomato"], 400, "kW", ["c","c-total"]))

graphs.append(Graph("Stan obriornik A", ["steelblue"], 150, "", ["a-state"]))
graphs.append(Graph("Stan obriornik B", ["steelblue"], 150, "", ["b-state"]))
graphs.append(Graph("Stan obriornik C", ["steelblue"], 150, "", ["c-state"]))

graphs.append(Graph("Stan boiler 1", ["lightseagreen"], 400, "", ["b0"]))
graphs.append(Graph("Stan boiler 2", ["lightseagreen"], 400, "", ["b1"]))

#Timespan selector 
selector = Select(title="Zakres danych", value=5, options=[
    ('1','1 min'),
    ('2','2 min'),
    ('3','3 min'),
    ('5','5 min'),
    ('10','10 min'),
    ('20','20 min'),
    ('30','30 min'),
    ('60','60 min'),
    ('120', '2 h'),
    ('240', '4 h'),
    ('360', '6 h'),
    ('480', '8 h'),
    ('720', '12 h'),
    ('1440', '24 h'),
    ('2880', '48 h')
])

def selectorUpdate(attr,old,new):
    selectedTime['value'] = int(new)

selector.on_change('value',selectorUpdate)

def update():
    #Reading recentData and agregatedData when it exists
    date = datetime.now().strftime("%Y-%m-%d")
    recentDataPATH = f"database/{date}-log.csv"
    agregatedDataPATH = "database/agrData.csv"

    recentData = pd.read_csv(recentDataPATH)
    if os.path.isfile(agregatedDataPATH):
        agregatedData = pd.read_csv(agregatedDataPATH)
        data = pd.concat([agregatedData, recentData], ignore_index=True)
    else:
        data = recentData

    #Formating time collumn as datetime
    data['time'] = pd.to_datetime(data['time'], format="%Y-%m-%d %H:%M:%S")
    #Calculating cuttof date base on selected timespan
    cuttofDate = datetime.now() - timedelta(minutes = selectedTime['value'])
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
                selector, 
                sizing_mode="stretch_width")

#Creating webpage and calling update function
curdoc().add_root(layout)
curdoc().add_periodic_callback(update, 1000)

#run with -> bokeh serve --show plotter.py