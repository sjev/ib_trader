#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

# Prototype of a real-time dashboard

## References

[Bokeh server] https://bokeh.pydata.org/en/latest/docs/user_guide/server.html#userguide-server

"""

# myapp.py

from random import random

from bokeh.layouts import column
from bokeh.models import Button
from bokeh.plotting import figure, curdoc
from bokeh.models import ColumnDataSource
from bokeh.models.widgets import DataTable, DateFormatter, TableColumn
import numpy as np




def generatePrice():
    symbols = ['AAA','BBB','CCC']
    prices = np.random.rand(len(symbols)).round(2)
    return dict(symbol=symbols,price=prices)

# make table 
data = generatePrice()
print('Data: ',data)
currentData = ColumnDataSource(data)
columns = [TableColumn(field="symbol",title="symbol"), TableColumn(field="price",title="price")]

tblPrices = DataTable(source=currentData,columns=columns,width=400, height=280)



def callback():
    # test button callback
    #currentData.stream(generatePrice())
    symbols = ['AAA','BBB','CCC']
    prices = np.random.rand(len(symbols)).round(2)
    
    data = [(idx,val) for idx,val in enumerate(prices)]
    print('patch: ',data)
    
    patch = {'price':data}
    print(patch)
    currentData.patch(patch)
    
    
   

# add a button widget and configure with the call back
button = Button(label="Press Me", button_type='primary')
button.on_click(callback)

# put the button and plot in a layout and add to the document
curdoc().add_root(column(button, tblPrices))