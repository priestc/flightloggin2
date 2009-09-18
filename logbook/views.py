from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.forms.models import modelformset_factory
from django.forms.formsets import formset_factory

from annoying.decorators import render_to
from annoying.functions import get_object_or_None
from share.decorator import no_share

from models import Flight, Columns
from forms import *
from constants import *
from totals import column_total_by_list
from profile.models import Profile

######################################################################################################################################

@render_to("logbook.html")
def logbook(request, shared, display_user, page=0):

    form = FlightForm()
    
    if request.POST:
        if request.POST.get('submit', "") == "Submit New Flight":
            flight = Flight(user=display_user)
            form = FlightForm(request.POST, instance=flight)
            
            if form.is_valid():
                form.save()
                return HttpResponseRedirect('/' + display_user.username + '/logbook.html')
            else:
                ERROR = "'new'"
                
        elif request.POST.get('submit', "") == "Edit Flight":
            flight_id = request.POST['id']
            flight = Flight(pk=flight_id, user=display_user)
            
            form = FlightForm(request.POST, instance=flight)
            
            if form.is_valid():
                form.save()
                return HttpResponseRedirect('/' + display_user.username + '/logbook.html')
            else:
                ERROR = "'edit'"
                
        elif request.POST.get('submit', "") == "Delete Flight":
            flight_id = request.POST['id']
            Flight(pk=flight_id, user=display_user).delete()           
            ERROR = 'false'
                
    ##############################################################
    try:
        profile = display_user.get_profile()
    except:
        profile = Profile()
        
    class LogbookRow(list):
        date = ""
        plane = ""
        pk = 0

    logbook = []
    
    if profile.minutes:
        format = "minutes"
    else:
        format = "decimal"
    
    if profile.date_format:
        date_format = profile.date_format
    else:
        date_format = "Y-m-d"
    
    from profile.models import AutoButton   
    auto_button,c = AutoButton.objects.get_or_create(user=display_user)
    
    all_flights = Flight.objects.user(display_user)
    flights = all_flights.select_related()
    columns, created = Columns.objects.get_or_create(user=display_user)

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
            row.plane = flight.plane

            for column in columns.as_list():
                if column == "date":
                    row.date = flight.column("date")
                    
                elif column == "remarks":
                    row.remarks = flight.column("remarks")
                    row.events = flight.column("events")
                else:
                    row.append( {"system": column, "disp": flight.column(column, format), "title": FIELD_TITLES[column]} )

            logbook.append(row)

        del flight, row, column
        
    overall_totals, totals_columns = column_total_by_list(all_flights, columns.as_list(), format=format)
    
    return locals()

#######################################################################################################################################

@no_share   
@login_required()
@render_to("mass_entry.html")     
def mass_entry(request, shared, display_user):
    
    try:
        profile = display_user.get_profile()
    except:
        profile = Profile()
        
    NewFlightFormset = modelformset_factory(Flight, form=FormsetFlightForm, extra=profile.per_page, formset=FixedPlaneModelFormset)
        
    if request.POST.get('submit'):
        post = request.POST.copy()
        for pk in range(0, profile.per_page):
            if post["form-" + str(pk) + "-date"]:
                post.update({"form-" + str(pk) + "-user": str(request.user.pk)})
            else:
                post.update({"form-" + str(pk) + "-user": u''})
            
        formset = NewFlightFormset(post, queryset=Flight.objects.get_empty_query_set(), planes_queryset=Plane.objects.filter(user__pk__in=[2147483647,display_user.id]))
        
        if formset.is_valid():
            for form in formset.forms:
                instance = form.save(commit=False)
                instance.user = display_user
                if instance.date:
                    instance.save()
            
            return HttpResponseRedirect('/' + display_user.username + '/logbook.html')
        
    else:
        formset = NewFlightFormset(queryset=Flight.objects.get_empty_query_set(), planes_queryset=Plane.objects.filter(user__pk__in=[2147483647,display_user.id]))

    return locals()

@no_share
@login_required()
@render_to("mass_entry.html")     
def mass_edit(request, share, display_user, page=0):
    edit = True 
    flights = Flight.objects.filter(user=display_user)
    
    try:
        profile = display_user.get_profile()
    except:
        profile = Profile()
        
    start = (int(page)-1) * int(profile.per_page)
    duration = int(profile.per_page)
    qs = Flight.objects.filter(user=display_user)[start:start+duration]
    NewFlightFormset = modelformset_factory(Flight, form=FormsetFlightForm, formset=FixedPlaneModelFormset, extra=0, can_delete=True)
        
    if request.POST.get('submit'):
        formset = NewFlightFormset(request.POST, queryset=qs, planes_queryset=Plane.objects.filter(user__pk__in=[2147483647,display_user.id]))
        
        if formset.is_valid():
            formset.save()
            return HttpResponseRedirect('/' + display_user.username + '/logbook.html')
    else:
        formset = NewFlightFormset(queryset=qs, planes_queryset=Plane.objects.filter(user__pk__in=[2147483647,display_user.id]))
    
    return locals()






















        
        
