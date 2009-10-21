from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.forms.models import modelformset_factory
from django.forms.formsets import formset_factory

from annoying.decorators import render_to
from share.decorator import no_share

from models import Flight, Columns
from forms import *
from constants import *
from totals import column_total_by_list
from profile.models import Profile, AutoButton

###############################################################################

@render_to("logbook.html")
def logbook(request, shared, display_user, page=0):

    form = FlightForm(prefix="new")
    
    if request.POST.get('submit', "") == "Submit New Flight":
        flight = Flight(user=display_user)
        form = FlightForm(request.POST, instance=flight, prefix="new")
        
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/' + display_user.username +
                '/logbook.html')
        else:
            ERROR = "'new'"
            
    elif request.POST.get('submit', "") == "Edit Flight":
        flight_id = request.POST['id']
        flight = Flight(pk=flight_id, user=display_user)
        
        form = FlightForm(request.POST, instance=flight, prefix="new")
        
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(request.path)
        else:
            ERROR = "'edit'"
            
    elif request.POST.get('submit', "") == "Delete Flight":
        flight_id = request.POST['id']
        Flight(pk=flight_id, user=display_user).delete()           
        ERROR = 'false'
        return HttpResponseRedirect(request.path)
        
    ##############################################################
    
    auto_button,c = AutoButton.objects.get_or_create(user=display_user)
    cols, c = Columns.objects.get_or_create(user=display_user)
    
    header_row = cols.header_row()
    
    columns = cols.all_list()          # all activated column headers
    prefix_len = cols.prefix_len()     # number of non-agg headers before total
    agg_columns = cols.agg_list()      # all headers that get agg'd
    
    ################## custom filter form ########################
    
    from custom_filter import make_filter_form
    FilterForm = make_filter_form(display_user)
    ff = FilterForm()
    
    ##############################################################
    
    all_flights = Flight.objects.user(display_user)
    
    if request.GET.get('c', "") == "t":
        ff=FilterForm(request.GET)
        flights = all_flights.custom_logbook_view(ff).select_related()
        all_flights = flights
        get= "?" + request.get_full_path().split('?')[1]
        total_sign = "Filter"
    else:
        flights = all_flights.select_related()
        total_sign = "Overall"
                
    ############## get user preferences ##########################
    
    profile = Profile.get_for_user(display_user)
    num_format = profile.get_format()
    date_format = profile.get_date_format()
    
    overall_totals = column_total_by_list(all_flights,
                                          agg_columns,
                                          format=num_format)
    
    if not flights:
        return locals()
    
    before_block, after_block, page_of_flights = \
                   Flight.make_pagination(flights, profile, int(page))

    ##############################################################
    
    from utils import LogbookRow
    
    LogbookRow = LogbookRow.set_formats(df=date_format, nf=num_format)
    
    logbook = []
    for flight in list(page_of_flights.object_list):
        row = LogbookRow(flight=flight, columns=columns)
        logbook.append(row)
    
    #only make the page table if there are more than one pages overall
    do_pagination = page_of_flights.paginator.num_pages > 1
    
    return locals()

###############################################################################

@no_share   
@login_required()
@render_to("mass_entry.html")     
def mass_entry(request, shared, display_user):
    
    try:
        profile = display_user.get_profile()
    except:
        profile = Profile()
        
    NewFlightFormset = modelformset_factory(Flight,
                                            form=FormsetFlightForm,
                                            extra=profile.per_page,
                                            formset=FixedPlaneModelFormset)
        
    if request.POST.get('submit'):
        post = request.POST.copy()
        for pk in range(0, profile.per_page):
            # if this line has no date...
            if post["form-%s-date" % pk]:
                # add the user 
                post.update({"form-%s-user" % pk: str(request.user.pk)})
            else:
                # blank the user
                post.update({"form-%s-user" % pk: u''})
            
        formset = NewFlightFormset(post,
                    queryset=Flight.objects.get_empty_query_set(),
                    planes_queryset=Plane.objects.user_common(display_user))
        
        if formset.is_valid():
            for form in formset.forms:
                instance = form.save(commit=False)
                instance.user = display_user
                if instance.date:
                    instance.save()
            
            return HttpResponseRedirect('/%s/logbook.html' % display_user)
        
    else:
        formset = NewFlightFormset(queryset=Flight.objects.get_empty_query_set(),
                    planes_queryset=Plane.objects.user_common(display_user))

    return locals()

@no_share
@login_required()
@render_to("mass_entry.html")     
def mass_edit(request, shared, display_user, page=0):
    edit = True 
    flights = Flight.objects.filter(user=display_user)
    
    try:
        profile = display_user.get_profile()
    except:
        profile = Profile()
        
    start = (int(page)-1) * int(profile.per_page)
    duration = int(profile.per_page)
    qs = Flight.objects.filter(user=display_user)[start:start+duration]
    NewFlightFormset = modelformset_factory(Flight, form=FormsetFlightForm,
            formset=FixedPlaneModelFormset, extra=0, can_delete=True)
        
    if request.POST.get('submit'):
        formset = NewFlightFormset(request.POST, queryset=qs,
                    planes_queryset=Plane.objects.user_common(display_user)
                  )
        
        if formset.is_valid():
            formset.save()
            return HttpResponseRedirect('/%s/logbook.html' % display_user)
    else:
        formset = NewFlightFormset(queryset=qs,
                    planes_queryset=Plane.objects.user_common(display_user),
                  )
    
    return locals()














        
        
