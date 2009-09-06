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

from annoying.decorators import render_to
from is_shared import is_shared
from datetime import date, timedelta
from logbook.models import Flight
from logbook.constants import FIELD_TITLES

from image_formats import plot_png, plot_svg
from format_ticks import format_line_ticks

@render_to('graphs.html')
def graphs(request, username):
    shared, display_user = is_shared(request, username)
    return locals()
    
    
def line(display_user, column, s=None, e=None):
    
    #kwargs = {str(column + "__gt"): 0}    
    
    if s and e:
        s = datetime.date(*[int(foo) for foo in s.split('.')])
        e = datetime.date(*[int(foo) for foo in e.split('.')])
        prev_total = Flight.nosim.filter(user=display_user, date__lt=s).aggregate(total=Sum(column))['total'] or 0
        flights = list(Flight.nosim.filter(user=display_user, date__gte=s, date__lte=e).values('date').annotate(value=Sum(column)).order_by('date'))
    else:
        prev_total = 0
        flights = list(Flight.nosim.filter(user=display_user).values('date').annotate(value=Sum(column)).order_by('date'))
        e = flights[-1]['date']
        s = flights[0]['date']
    
    
    year_range = (e-s).days / 365.0 #subtract both dates, convert timedelta to days, divide by 365 = X.XX years
    
    dates=[]
    values=[]
    for day in flights:
        values.append(day['value'])
        dates.append(day['date'])
        
    values[0] = values[0] + prev_total
    acc_values = np.cumsum(values)
    
    #assert False, prev_total
    
    ####################################################################
    
    fig = plt.figure()
    
    df = "F jS, Y"
    sub = "From %s to %s" % (dj_date_format(s, df), dj_date_format(e, df))
    fig.suptitle(r'\textit{Velocity (5/sec)}' )#%s%s' % (FIELD_TITLES[column], sub), fontsize=18)
    
    ax = fig.add_subplot(111)
    ax.plot(dates, acc_values, '-', drawstyle='steps')
    ax.set_xlim(s, e)
    
    format_line_ticks(ax, year_range)
    
    ax.set_ylabel('Flight Hours')

    # format the coords message box
    def price(x): return '$%1.1f'%x
    ax.format_xdata = mdates.DateFormatter('%Y-%m-%d')
    ax.format_ydata = price
    ax.grid(True)

    # rotates and right aligns the x labels, and moves the bottom of the
    # axes up to make room for them
    fig.autofmt_xdate()

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
    










def line_generator(request, username, column, s=None, e=None, ext=None):
    shared, display_user = is_shared(request, username)
    
    if ext == "png":
        line2 = plot_png(line)
        
    if ext == "svg":
        line2 = plot_svg(line)
        
    return line2(display_user, column, s, e)
