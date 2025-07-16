from bokeh.layouts import column, row
from bokeh.models import ColumnDataSource, Select
from bokeh.plotting import figure, curdoc
import pandas as pd
from datetime import datetime, timedelta

dataPath = "data.csv"
selectedTime = {"value":5}

source = ColumnDataSource(data=dict(x=[], y=[]))

productionFigure = figure(title="production",x_axis_type="datetime" ,x_axis_label="time", y_axis_label="kW")
productionFigure.line(x='x',y='y', source=source, line_width=2)
productionFigure.sizing_mode="stretch_width"

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
    source.data = dict(x=data['time'], y=data['prod'])

layout = column(productionFigure, selector, sizing_mode="stretch_width")

curdoc().add_root(layout)
curdoc().add_periodic_callback(update, 1000)

#run with: bokeh serve --show plotter.py