from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.http import HttpResponseRedirect
from django.forms import ModelForm
from django.core.paginator import Paginator, InvalidPage, EmptyPage

from annoying.decorators import render_to
from annoying.functions import get_object_or_None

from models import Flight, Columns
from forms import *
from constants import *
from totals import total_column
from profile.models import Profile



@login_required()
@render_to("logbook.html")
def logbook(request, page=0):
    title="Logbook"
    
    #####################################################
    
    form = FlightForm(planes_queryset=Plane.objects.filter(user__pk__in=[2147483647,request.user.id]))
    
    if request.POST.get('submit', "") == "Submit New Flight":
        flight = Flight(user=request.user)
        form = FlightForm(request.POST, instance=flight, planes_queryset=Plane.objects.filter(user__pk__in=[2147483647,request.user.id]))
     
    elif request.POST.get('submit', "") == "Edit Flight":
        flight_id = request.POST['id']
        flight = Flight(pk=flight_id, user=request.user)
        
        form = FlightForm(request.POST, instance=flight, planes_queryset=Plane.objects.filter(user__pk__in=[2147483647,request.user.id]))
        
    if request.POST and form.is_valid():
        form.save()
        return HttpResponseRedirect('/logbook/')
    
    ##############################################################
    try:
        profile = request.user.get_profile()
    except:
        profile = Profile()
        
    class LogbookRow(list):
        date = ""
        plane = ""
        route = ""
        raw_route = ""
        pk = 0

    logbook = []
    
    if profile.minutes:
        format = "minutes"
    else:
        format = "decimal"
    
    
    all_flights = Flight.objects.filter(user=request.user)
    flights = all_flights.select_related()
    columns, created = Columns.objects.get_or_create(user=request.user)
    
    
    

    if flights:
    
        ###################
        
        page = int(page)

        paginator = Paginator(flights, per_page=profile.per_page, orphans=5)		#define how many flights will be on each page

        try:
            page_of_flights = paginator.page(page)				#get the pertinent page

        except (EmptyPage, InvalidPage):
            page_of_flights = paginator.page(paginator.num_pages)		#if that page is invalid, use the last page
            page = paginator.num_pages

        do_pagination = paginator.num_pages > 1					#if there is only one pago, do not make the pagination table

        before_block = range(1, page)[-5:]                       # a list from 1 to the page number, limited to the 5th from last to the end
        after_block = range(page, paginator.num_pages+1)[1:6]    # a list from the current page to the last page, limited to the first 5 items
	    
	    #####################
        
        for flight in page_of_flights.object_list:
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
        
    overall_totals, totals_columns = total_column(all_flights, columns.as_list(), format=format)
    #assert False
    
    return locals()
    

    
    
    
    
@login_required()   
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

    
@login_required()
@render_to("mass_entry.html")     
def mass_entry(request, page=0):
    return locals()
























        
        
