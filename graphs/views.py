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
from logbook.constants import FIELD_TITLES
from logbook.utils import sim

from image_formats import plot_png, plot_svg
from format_ticks import format_line_ticks

@render_to('graphs.html')
def graphs(request, username):
    shared, display_user = is_shared(request, username)
    from logbook.constants import AGG_FIELDS, FIELD_TITLES
    
    column_options = []
    for field in AGG_FIELDS:
        column_options.append("<option value=\"%s\">%s</option>" % (field, FIELD_TITLES[field] ) )
        
    column_options = mark_safe("\n".join(column_options))
    #assert False
    return locals()
    
    
def line(display_user, column, s=None, e=None):
    
    #kwargs = {str(column + "__gt"): 0}    
    
    if s and e:
        padding=datetime.timedelta(days=1)
        s = datetime.date(*[int(foo) for foo in s.split('.')])
        e = datetime.date(*[int(foo) for foo in e.split('.')])
        prev_total = Flight.objects.exclude(sim).filter(user=display_user, date__lt=s-padding).aggregate(total=Sum(column))['total'] or 0
        flights = list(Flight.objects.exclude(sim).filter(user=display_user, date__gte=s-padding, date__lte=e+padding).values('date').annotate(value=Sum(column)).order_by('date'))
        #import pdb; pdb.set_trace()
        flights.insert(0, {"date": s-datetime.timedelta(days=1), "value": prev_total})
        #assert False
    else:
        prev_total = 0
        flights = list(Flight.objects.exclude(sim).filter(user=display_user).values('date').annotate(value=Sum(column)).order_by('date'))
        e = flights[-1]['date']
        s = flights[0]['date']
    
    
    year_range = (e-s).days / 365.0 #subtract both dates, convert timedelta to days, divide by 365 = X.XX years
    
    dates=[]
    values=[]
    for day in flights:
        values.append(day['value'])
        dates.append(day['date'])
        
    #values.append(prev_total)
    #dates.append(
    acc_values = np.cumsum(values)
    
    #assert False, prev_total
    
    ####################################################################
    
    fig = plt.figure()
    
    d_color='#c14242'
    ax = fig.add_subplot(111)

    ax2 = ax.twinx()
    
    ax2.plot(dates, values, color=d_color)
    for tl in ax2.get_yticklabels():
        tl.set_color(d_color)
    
    ax.plot(dates, acc_values, '-', drawstyle='steps', lw=2)
    ax.set_xlim(s, e)
    
    

    
    df = "F jS, Y"
    sub = "From %s to %s" % (dj_date_format(s, df), dj_date_format(e, df))
    plt.figtext(.5,.94,'%s Progession' % (FIELD_TITLES[column]), fontsize=18, ha='center')
    plt.figtext(.5,.91,sub,fontsize=10,ha='center')
    
    format_line_ticks(ax, year_range)                      # format the ticks based on the range of the dates
    
    if column in ['day_l', 'night_l']:
        ax.set_ylabel('%ss' % FIELD_TITLES[column] )       #add "s" to the end
    elif column == "app":
        ax.set_ylabel('%ses' % FIELD_TITLES[column] )      #add "es" to the end
    else:
        ax.set_ylabel('Flight Hours' )
        ax2.set_ylabel('Flight Hours per day', color=d_color)



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
    










def line_generator(request, username, column, s=None, e=None, ext=None):
    shared, display_user = is_shared(request, username)
    
    if ext == "png":
        line2 = plot_png(line)
        
    if ext == "svg":
        line2 = plot_svg(line)
        
    return line2(display_user, column, s, e)
