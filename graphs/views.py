from django.http import HttpResponse

from annoying.decorators import render_to
from is_shared import is_shared
from datetime import date, timedelta
from logbook.models import Flight

from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas

def image_output(fig):
    canvas=FigureCanvas(fig)
    response=HttpResponse(content_type='image/png')
    canvas.print_png(response)
    return response


def datetimeRange(from_date, to_date=None):
    while to_date is None or from_date <= to_date:
        yield from_date
        from_date = from_date + timedelta(days = 1)


@render_to('graphs.html')
def graphs(request, username):
    shared, display_user = is_shared(request, username)
    return locals()
    
def histogram(request, column):
    display_user = request.user
    kwargs = {str(column + "__gt"): "0"}
    flights = Flight.objects.filter(user=display_user, **kwargs).values_list(column, flat=True)
    #assert False
    
    #from django.db.models import Max, Min, Sum
    #agg = flights.aggregate(Max('date'), Min('date'), Sum(column), )
    #end = agg['date__max']
    #start=agg['date__min']
    
    #results = {}
    #for f in flights:
    #    results[f.date] = f.total
            
    # len(results)
    
    #data = [results.get(day, 0) for day in datetimeRange(start, end)]
    #dates= [day in datetimeRange(start, end)]
    
    #del results
    
    ################################################################
    
    from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
    from matplotlib.figure import Figure
    from matplotlib.dates import DateFormatter
    
    fig = Figure()
    ax = fig.add_subplot(111)
    
    #ax.plot_date(dates, data, '-')
    ax.hist(flights, normed=1, facecolor='green', alpha=0.75)
    
    #ax.xaxis.set_major_formatter(DateFormatter('%Y-%m-%d'))
    
    #################################################
    return image_output(fig)
    
def line(request, column):
    display_user = request.user
    kwargs = {} #{str(column + "__gt"): "0"}
    flights = Flight.objects.filter(user=display_user, **kwargs).order_by('-date')
    
    from django.db.models import Max, Min, Sum
    agg = flights.aggregate(Max('date'), Min('date'), Sum(column), )
    end = agg['date__max']
    start=agg['date__min']
    
    r={}
    for f in flights[:13]:
        r[f.date] = f.total
    
    import datetime
    import numpy as np
    import matplotlib
    import matplotlib.pyplot as plt
    import matplotlib.dates as mdates
    import matplotlib.mlab as mlab

    years    = mdates.YearLocator()   # every year
    months   = mdates.MonthLocator()  # every month
    yearsFmt = mdates.DateFormatter('%m-%Y')

    # load a numpy record array from yahoo csv data with fields date,
    # open, close, volume, adj_close from the mpl-data/example directory.
    # The record array stores python datetime.date as an object array in
    # the date column
    #datafile = matplotlib.get_example_data('goog.npy')
    #r = np.load(datafile).view(np.recarray)
    
    
    dates = [
        datetime.date(2004, 4,13),
        datetime.date(2004, 4,13),
        datetime.date(2004, 4,13),
        datetime.date(2007, 1,13),
        datetime.date(2008, 7,13)]
    

    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.plot(r.keys(), r.values())


    # format the ticks
    ax.xaxis.set_major_locator(years)
    ax.xaxis.set_major_formatter(yearsFmt)
    ax.xaxis.set_minor_locator(months)

    #datemin = datetime.date(start, 1, 1)
    #datemax = datetime.date(end, 1, 1)
    ax.set_xlim(start, end)

    # format the coords message box
    def price(x): return '$%1.2f'%x
    ax.format_xdata = mdates.DateFormatter('%Y-%m-%d')
    ax.format_ydata = price
    ax.grid(True)

    # rotates and right aligns the x labels, and moves the bottom of the
    # axes up to make room for them
    fig.autofmt_xdate()

    #################################################
    
    return image_output(fig)
    

