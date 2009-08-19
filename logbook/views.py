from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.http import HttpResponseRedirect
from django.forms import ModelForm


from annoying.decorators import render_to
from annoying.functions import get_object_or_None

from models import Flight, Columns
from forms import *
from constants import *

@login_required()
@render_to("logbook.html")
def logbook(request, page=0):
    title="Logbook"
    
    #####################################################
    
    form = FlightForm(planes_queryset=Plane.objects.filter(user__pk__in=[2147483647,request.user.id]))
    
    if request.POST.get('submit', "") == "Submit New Flight":
        flight = Flight(user=request.user)
        form = FlightForm(request.POST, instance=flight, planes_queryset=Plane.objects.filter(user__pk__in=[2147483647,request.user.id]))
        
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/logbook/')
     
    if request.POST.get('submit', "") == "Edit Flight":
        flight_id = request.POST['id']
        flight = Flight(pk=flight_id, user=request.user)
        
        form = FlightForm(request.POST, instance=flight, planes_queryset=Plane.objects.filter(user__pk__in=[2147483647,request.user.id]))
        
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/logbook/')
    
    ##############################################################
    
    flights = Flight.objects.filter(user=request.user)
    columns = get_object_or_None(Columns, user=request.user)

    if not columns:
        columns=Columns(user=request.user)

    class LogbookRow(list):
        date = ""
        plane = ""
        route = ""
        raw_route = ""
        pk = 0

    logbook = []
    format = "minutes"

    if flights:
        for flight in flights:
            row = LogbookRow()
            
            row.pk = flight.pk

            for column in columns.as_list():
                if column == "date":
                    row.date = flight.column("date")

                elif column == "plane":
                    row.plane = flight.column("plane")

                elif column == "route":
                    row.route = flight.column("route")
                    if flight.route:                                        # dont try to get fallback string if there is no route, (attribute error)
                        row.raw_route = flight.route.fallback_string
                    
                elif column == "remarks":
                    row.remarks = flight.column("remarks")
                    row.events = flight.column("events")
                else:
                    row.append( {"system": column, "disp": flight.column(column, format), "title": FIELD_TITLES[column]} )

            logbook.append(row)

        del flight, row, column
        
    args = []
    asl = columns.as_list()
    for field in columns.as_list():
        if field in AGG_FIELDS:
            args.append(Sum(field))

    overall_totals = Flight.objects.filter(user=request.user).aggregate(*args).values()
    #assert False
    return locals()
    
def backup(request):
    import csv
    from django.http import HttpResponse
    from records.models import Records

    response = HttpResponse(mimetype='text/plain')
    #response['Content-Disposition'] = 'attachment; filename=somefilename.csv'
    
    flights = Flight.objects.filter(user=request.user)
    planes = Plane.objects.filter(user=request.user)

    writer = csv.writer(response, dialect='excel')
    writer.writerow([FIELD_TITLES[field] for field in BACKUP_FIELDS])
    
    for flight in flights:
        writer.writerow([flight.column(field) for field in BACKUP_FIELDS])
        
    writer.writerow(["#####RECORDS"])
    
    records = get_object_or_None(Records, user=request.user)
    if records:
        writer.writerow([records.text])
        
    writer.writerow(["#####PLANES"])
        
    for p in planes:
        writer.writerow([p.tailnumber, p.manufacturer, p.model, p.cat_class, " ".join(p.get_tags_quote())])

    return response

    
       

























        
        
