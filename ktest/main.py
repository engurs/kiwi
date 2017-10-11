# -*- coding: utf-8 -*-
from bokeh.io import curdoc, show,output_file
from bokeh.models import  ColumnDataSource,Range1d
from bokeh.plotting import Figure
from bokeh.models.widgets import Select
from bokeh.layouts import row, column


import numpy as np
import pandas as pd
from datetime import datetime,timedelta


""" Test first 1000 data """
with open('report.csv', 'r') as csv_file:
    data = pd.read_csv("report.csv")[:1000]

source = ColumnDataSource(dict(
    timest=[],
    id=[],
    type=[],
    status=[],
    y=[]

))

print "source"
print source



csv_timestamp = [x for x in data['timestamp'] ]
csv_id = [x for x in data['id']]
csv_type = [x for x in data['type']]
csv_status = [x for x in data['status']]

print "timestamp"
print csv_timestamp
print "id"
print id
print "type"
print csv_type
print "status"
print csv_status




i = 0
date_list = []
d = {}  #id_freq
print "i"
print i
print  "date_list"
print  date_list
print "d"
print d

""" Create stream chart """
fig = Figure(x_axis_type='datetime')
fig.line(source=source, x="timest", y="y", color="red")

""" Select a date """
select = Select(title="Date:", options=[])

#################################

next_moment = datetime.strptime(csv_timestamp[i], '%Y-%m-%dT%H:%M:%SZ')
print "next_moment"
print next_moment

""" Create a bar chart """
top_10 = ["a", "b", "c"]
f = Figure(x_range=top_10)
######################


def update_chart(attr, old, new):

    print  "UPDATE_CHART FUNC"
    """ Get 10 ID  """
    global i
    top_10 = ["a", "b", "c"]
    f.x_range.factors = sorted(d[select.value], key=d[select.value].get)[::-1][:10]

    print "f_xrange_fac"
    print sorted(d[select.value], key=d[select.value].get)[::-1][:10]

    l =sorted(d[select.value], key=d[select.value].get)[::-1][:10]
    """ Create a bar for the selected date """
    print "l"
    print l

    f.vbar(bottom=0, color='blue',top = sorted((d[select.value]).values())[::-1][:10], x = [x + ":0.65" for x in l], legend="Selected Date", width=0.3)

    """ Date of  one week ago"""

    selectedValueDatetime=datetime.strptime(select.value, "%Y-%m-%d").date()
    print "selectedValueDatetime"
    print selectedValueDatetime

    print "selected dates values"
    print sorted((d[select.value]).values())[::-1][:10]
    print sorted((d[str(selectedValueDatetime)]).values())[::-1][:10]


##################### 1 gün öncesi ##################
    AWeekAgo = selectedValueDatetime - timedelta(1)
###################
    print "AWeekAgo"
    print AWeekAgo

    """  NO VALUE bar"""
    if str(AWeekAgo) not in d.keys():
        ValuesofAWeekAgo = 10*[0]
    else:
        ValuesofAWeekAgo = sorted((d[str(AWeekAgo)]).values())[::-1][:10]




    print "ValuesofAWeekAgo"
    print ValuesofAWeekAgo

    """Create a week ago bar """
    f.vbar(bottom=0, color='green', top=ValuesofAWeekAgo, x=[x + ":0.35" for x in l], legend='A Week Ago', width=0.3 )

    #print type(select.value)
    i += 1



def update_data():
    print "UPDATE_DATA FUNC"
    global i
    """ Pull the next date """
    next_moment = datetime.strptime(csv_timestamp[i], '%Y-%m-%dT%H:%M:%SZ')

    print "next_moment"
    print  next_moment

    print "next_moment.date"
    print next_moment.date()

    """ Update options for the dropdown menu """
    if str(next_moment.date()) not in date_list:
        date_list.append(str(next_moment.date()))
        select.options = date_list  # sorted(set(date_list)) ?? =
        print "date_list"
        print date_list

    """ Trig the bar"""

    d.update({str(next_moment.date())  :  {x  : (csv_id[:i+1]).count(x) for x in set(csv_id[:i+1])}})

    i += 1
    new_data = dict(timest=[next_moment],  y=[i],  id=[csv_id[i]], type=[csv_type[i]], status=[csv_status[i]])

    print  "new_data"
    print new_data

    source.stream(new_data)



select.on_change("value", update_chart)



controls = column(select,f)
curdoc().add_root(column(controls,fig))
curdoc().add_periodic_callback(update_data, 10)
#curdoc().remove_root(f)





