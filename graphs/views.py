from django.http import HttpResponse

from annoying.decorators import render_to
from is_shared import is_shared
from datetime import date, timedelta
from logbook.models import Flight

def datetimeRange(from_date, to_date=None):
    while to_date is None or from_date <= to_date:
        yield from_date
        from_date = from_date + timedelta(days = 1)


@render_to('graphs.html')
def graphs(request, username):
    shared, display_user = is_shared(request, username)
    
    return locals()
    
def test2():
    flights = Flight.objects.filter(user=display_user)
    
    from django.db.models import Max, Min, Sum
    agg = flights.aggregate(Max('date'), Min('date'), Sum('pic'), )
    end = agg['date__max']
    start=agg['date__min']
    
    results = {}
    for f in flights:
        results[f.date] = f.total
        
    data = []
    for day in datetimeRange(start, end):
        try:
            last = data[-1]
        except:
            last = 0

        data.append(results.get(day, 0) + last)
        
    del results
    
    ################################################################
    
    from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
    from matplotlib.figure import Figure
    from matplotlib.dates import DateFormatter
    
    
    
    #################################################
    canvas=FigureCanvas(fig)
    response=HttpResponse(content_type='image/png')
    canvas.print_png(response)
    
def test(request):
    import random
    import datetime
    
    

    fig=Figure()
    ax=fig.add_subplot(111)
    x=[]
    y=[]
    now=datetime.datetime.now()
    delta=datetime.timedelta(days=1)
    for i in range(10):
        x.append(now)
        now+=delta
        y.append(random.randint(0, 1000))
    ax.plot_date(x, y, '-')
    ax.xaxis.set_major_formatter(DateFormatter('%Y-%m-%d'))
    fig.autofmt_xdate()

    return response

