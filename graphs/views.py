import datetime
import numpy as np

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.ticker as ticker
import matplotlib.mlab as mlab

from matplotlib.figure import Figure
from matplotlib.dates import DateFormatter

from django.db.models import Max, Min, Sum
from django.utils.dateformat import format as dj_date_format
from django.utils.safestring import mark_safe

from annoying.decorators import render_to
from is_shared import is_shared
from datetime import date, timedelta
from logbook.models import Flight
from logbook.constants import *

from image_formats import plot_png, plot_svg
from format_ticks import format_line_ticks

from logbook.constants import AGG_FIELDS, EXTRA_AGG, FIELD_TITLES

def datetimeRange(from_date, to_date=None):
    while to_date is None or from_date <= to_date:
        yield from_date
        from_date = from_date + timedelta(days = 1)


@render_to('graphs.html')
def graphs(request, username):
    shared, display_user = is_shared(request, username)
    
    
    column_options = []
    for field in GRAPH_FIELDS:
        column_options.append("<option value=\"%s\">%s</option>" % (field, FIELD_TITLES[field] ) )
        
    column_options = mark_safe("\n".join(column_options))
    #assert False
    return locals()
    
############################################################################################################################################
############################################################################################################################################
    
def progress_rate(display_user, column, s=None, e=None):

    for column in [column]:
        
        if column in DB_FIELDS:
            db_column = column
            
        elif column in PIC_FIELDS:
            db_column = 'pic'
        else:
            db_column = 'total'
            
        qs=Flight.objects.user(display_user)                ## starting queryset
        
        if s and e:
            assert e > s        #start time is before end time or else code 500 error
            pad=datetime.timedelta(days=1)
            s = datetime.date(*[int(foo) for foo in s.split('.')])
            e = datetime.date(*[int(foo) for foo in e.split('.')])

            flights = qs.filter_by_column(column).filter(date__lt=e+pad, date__gt=s-pad).values('date').annotate(value=Sum(db_column)).order_by('date')
            
            before_graph = qs.filter(date__lt=s-pad)        ## all stuff before the graph begins
            
            prev_total = before_graph.agg(column)
        else:
            prev_total = 0
                 
            flights = qs.filter_by_column(column).values('date').annotate(value=Sum(db_column)).order_by('date')
        
        flights=list(flights)

        if not (s and e):
            e = flights[-1]['date']
            s = flights[0]['date']
        else:
            flights.insert(0, {"date": s-datetime.timedelta(days=1), "value": prev_total})
    
    dates=[]
    values=[]
    dict = {}
    for day in flights:
        values.append(day['value'])
        dates.append(day['date'])
        dict.update({day['date']: day['value']})
    
    ############## make accumulation plot
       
    acc_values = np.cumsum(values)
    
    ############## make rate plot
    
    padded = [dict.get(day, 0) for day in datetimeRange(s, e)]   #with zeroes for days that have no flights logged

    month_avg=[]
    padding_dates=[]
    date=s
    r=30   #range, 30 days
    for i, day in enumerate(padded):
        bottom = i-r
        if bottom < 0:      #don't allow negative indexes, this is not what we want
            bottom=0
            
        month_avg.append(  sum(padded[bottom:i])  )
        date += datetime.timedelta(days=1)
        padding_dates.append(date)

    ############ format graph variables
    
    title = '%s Progession' % FIELD_TITLES[column]
    
    df = "F jS, Y"
    subtitle = "From %s to %s" % (dj_date_format(s, df), dj_date_format(e, df))
    
    if column in ['day_l', 'night_l', 'app']:
        acc_unit = '%s' % FIELD_TITLES[column]
        rate_unit = '%s per month' % FIELD_TITLES[column]
    else:
        acc_unit = 'Flight Hours'
        rate_unit = 'Flight Hours per month'
        
    plot1={"x": dates,
           "y": acc_values,
           "y_unit": acc_unit,
           "color": "b"}
           
    plot2={"x": padding_dates,
           "y": month_avg,
           "y_unit": rate_unit,
           "color": '#c14242'}
    
    return line_plot("twin", title, subtitle, s, e, plot1, plot2)
    
############################################################################################################################################
############################################################################################################################################

def line_plot(twin, title, subtitle, s, e, *plots):
    
    x=[]
    y=[]
    for plot in plots:       #each plot, there might be many
        x.append(plot["x"])
        y.append(plot["y"])
        
    year_range = (e-s).days / 365.0                      #subtract both dates, convert timedelta to days, divide by 365 = X.XX years
    
    fig = plt.figure()
    
    
    if twin == "twin":
        plot1 = plots[0]
        plot2 = plots[1]
        
        ax = fig.add_subplot(111)
        ax.plot(plot1['x'], plot1['y'], color=plot1['color'], drawstyle='steps-post', lw=2)
        ax.set_ylabel( plot1['y_unit'] )
        ax.set_xlim(s, e)
        
        ax2 = ax.twinx()
        d_color='#c14242'
        ax2.plot(plot2['x'], plot2['y'], color=plot2['color'], drawstyle='default')
        ax2.set_ylabel( plot2['y_unit'], color=plot2['color'], )
        for tl in ax2.get_yticklabels():
            tl.set_color(d_color)
    
    ax2.set_xlim(s, e)
    
    

    
    plt.figtext(.5,.94,title, fontsize=18, ha='center')
    plt.figtext(.5,.91,subtitle,fontsize=10,ha='center')
    
    format_line_ticks(ax, plt, year_range)                      # format the ticks based on the range of the dates

    # format the coords message box
    #def price(x): return '$%1.1f'%x
    #ax.format_xdata = mdates.DateFormatter('%Y-%m-%d')
    #ax.format_ydata = price
    ax.grid(True)

    # rotates and right aligns the x labels, and moves the bottom of the
    # axes up to make room for them
    #fig.autofmt_xdate()

    #################################################
    
    return fig
    
   
def histogram(request, column):
    display_user = request.user
    kwargs = {str(column + "__gt"): "0"}
    flights = Flight.objects.filter(user=display_user, **kwargs).values_list(column, flat=True)

    
    #del results
    
    ################################################################
    
    fig = Figure()
    ax = fig.add_subplot(111)
    
    ax.hist(flights, normed=1, facecolor='green', alpha=0.75)
    
    #ax.xaxis.set_major_formatter(DateFormatter('%Y-%m-%d'))
    
    #################################################
    return fig
    










def line_generator(request, username, type, column, s=None, e=None, ext=None):
    shared, display_user = is_shared(request, username)
    
    if type=="pr":
        func = progress_rate
        
    elif type=="mp":
        func = multiple_progress
        
    elif type=="mp":
        func = multiple_rate
    
    #######
    
    if ext == "png":
        line2 = plot_png(func)     #decorate function to output to the appropriate format
        
    elif ext == "svg":
        line2 = plot_svg(func)
        
    return line2(display_user, column, s, e)








