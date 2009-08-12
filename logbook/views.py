from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.contrib.auth.decorators import login_required
from django.db.models import Sum

from annoying.decorators import render_to
from annoying.functions import get_object_or_None

from models import Flight, Columns
from forms import *
#from constants import *

@login_required()
@render_to("logbook.html")
def logbook(request, page=0):
    title="Logbook"
    flights = Flight.objects.filter(user=request.user)
    flightform = FlightForm()
    columns = get_object_or_None(Columns, user=request.user)

    if not columns:
        columns=Columns(user=request.user)

    class LogbookRow(list):
        date = ""
        plane = ""
        route = ""

    logbook = []

    if flights:
        for flight in flights:
            row = LogbookRow()

            for column in columns.as_list():
                if column == "date":
                    row.date = flight.column(column)

                elif column == "plane":
                    row.plane = flight.column(column)

                elif column == "route":
                    row.route = flight.column(column)
                else:
                    row.append( {"title": column, "disp": flight.column(column)} )

            logbook.append(row)

        del flight, row, column

    #assert False
   
    args = []
    for field in columns.as_list():
        if field in AGG_FIELDS:
            args.append(Sum(field))

    overall_totals = Flight.objects.filter(user=request.user).aggregate(*args)



    return locals()
