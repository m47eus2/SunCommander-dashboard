from bokeh.layouts import column, row
from bokeh.models import ColumnDataSource, Select
from bokeh.plotting import figure, curdoc
import pandas as pd
from datetime import datetime, timedelta

class Graph():
    def __init__(self, title, colors, height, csvColumns):

        self.sources = []
        for column in csvColumns:
            self.sources.append(ColumnDataSource(data=dict(x=[],y=[])))

        self.figure = figure(title=title,x_axis_type="datetime",x_axis_label="Time", y_axis_label="kW", height=height)

        for i in range(len(csvColumns)):
            self.figure.line(x='x', y='y', source=self.sources[i], color=colors[i], line_width=2)

        self.figure.sizing_mode = "stretch_width"
        self.csvColumns = csvColumns
    
    def update(self, data):
        for i in range(len(self.csvColumns)):
            self.sources[i].data = dict(x=data["time"], y=data[self.csvColumns[i]])

dataPath = "data.csv"
selectedTime = {"value":5}

#Graphs
graphs = []

graphs.append(Graph("Production", ["limegreen"], 500, ["prod"]))

graphs.append(Graph("Energy", ["dodgerblue"], 500,["energy"]))
graphs.append(Graph("Accumulated energy", ["dodgerblue"], 500, ["cEnergy"]))

graphs.append(Graph("Receiver A", ["darkslateblue"], 400, ["ra"]))
graphs.append(Graph("Receiver B", ["darkslateblue"], 400, ["rb"]))
graphs.append(Graph("Receiver C", ["darkslateblue"], 400, ["rc"]))

graphs.append(Graph("Receiver A state", ["blue"], 200, ["sa"]))
graphs.append(Graph("Receiver B state", ["blue"], 200, ["sb"]))
graphs.append(Graph("Receiver C state", ["blue"], 200, ["sc"]))

graphs.append(Graph("Boiler 1", ["lightseagreen"], 400, ["b1"]))
graphs.append(Graph("Boiler 2", ["lightseagreen"], 400, ["b2"]))

#Timespan selector 
selector = Select(title="Zakres danych", value=5, options=[
    ('1','1 min'),
    ('2','2 min'),
    ('3','3 min'),
    ('5','5 min'),
    ('10','10 min'),
    ('20','20 min'),
    ('30','30 min'),
    ('60','60 min')
])

def selectorUpdate(attr,old,new):
    selectedTime['value'] = int(new)

selector.on_change('value',selectorUpdate)

def update():
    data = pd.read_csv(dataPath)
    data = data.tail(3600)
    data['time'] = pd.to_datetime(data['time'], format="%Y-%m-%d %H:%M:%S")
    cuttofDate = datetime.now() - timedelta(minutes = selectedTime['value'])
    data = data[data['time'] >= cuttofDate]

    for graph in graphs:
        graph.update(data)

layout = column(graphs[0].figure, 
                row(graphs[1].figure, graphs[2].figure, sizing_mode="stretch_width"),
                row(graphs[3].figure, graphs[4].figure, graphs[5].figure, sizing_mode="stretch_width"),
                row(graphs[6].figure, graphs[7].figure, graphs[8].figure, sizing_mode="stretch_width"),
                row(graphs[9].figure, graphs[10].figure, sizing_mode="stretch_width"),
                selector, 
                sizing_mode="stretch_width")

curdoc().add_root(layout)
curdoc().add_periodic_callback(update, 1000)

#run with -> bokeh serve --show classPlotter.py