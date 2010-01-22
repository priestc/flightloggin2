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

@no_share('logbook')
@render_to("logbook.html")
def logbook(request, page=0):
    
    form = FlightForm(prefix="new")
    
    if request.POST.get('submit', "") == "Submit New Flight":
        flight = Flight(user=request.display_user)
        form = FlightForm(request.POST, instance=flight, prefix="new")
        edit_or_new = "new"
        
        if form.is_valid():
            form.save()
            from backup.models import edit_logbook
            edit_logbook.send(sender=request.display_user)
            from django.core.urlresolvers import reverse
            url = reverse('logbook', kwargs={"username": request.display_user.username})
            return HttpResponseRedirect(url)
            
    elif request.POST.get('submit', "") == "Edit Flight":
        flight_id = request.POST['id']
        flight = Flight(pk=flight_id, user=request.display_user)
        form = FlightForm(request.POST, instance=flight, prefix="new")
        edit_or_new = "edit"
        
        if form.is_valid():
            form.save()
            from backup.models import edit_logbook
            edit_logbook.send(sender=request.display_user)
            return HttpResponseRedirect(request.path)
            
    elif request.POST.get('submit', "") == "Delete Flight":
        flight_id = request.POST['id']
        Flight(pk=flight_id, user=request.display_user).delete()
        return HttpResponseRedirect(request.path)
        
    ##############################################################
    
    auto_button,c = AutoButton.objects.get_or_create(user=request.display_user)
    cols, c = Columns.objects.get_or_create(user=request.display_user)
    profile,c = Profile.objects.get_or_create(user=request.display_user)
    
    ################## custom filter form ########################
    
    from custom_filter import make_filter_form
    ## filter form is created dynamically because each user has different planes
    ## so those dropdowns will be different
    FilterForm = make_filter_form(request.display_user)
    ff = FilterForm()
    
    ##############################################################
    
    all_flights = Flight.objects.filter(user=request.display_user)
    filtered_flights = all_flights.select_related()
    total_sign = "Overall"
    
    if request.GET:
        ff=FilterForm(request.GET)
        filtered_flights = filtered_flights.custom_logbook_view(ff)
        get= "?" + request.get_full_path().split('?')[1]
        total_sign = "Filter"
            
    ############## get user preferences ##########################
    
    before_block, after_block, page_of_flights = \
                   Flight.make_pagination(filtered_flights, profile, int(page))
    
    #only make the page table if there are more than one pages overall
    do_pagination = page_of_flights.paginator.num_pages > 1
    
    
    
    return locals()

###############################################################################

@no_share('NEVER')
@render_to("mass_entry.html")     
def mass_entry(request):
    
    try:
        profile = request.display_user.get_profile()
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
                    planes_queryset=Plane.objects.user_common(request.display_user))
        
        if formset.is_valid():
            for form in formset.forms:
                instance = form.save(commit=False)
                instance.user = request.display_user
                if instance.date:
                    instance.save()
                    
            # send signal
            from backup.models import edit_logbook
            edit_logbook.send(sender=request.display_user)
            
            from django.core.urlresolvers import reverse
            return HttpResponseRedirect(
                reverse('logbook', kwargs={"username": request.display_user.username})
            )
        
    else:
        formset = NewFlightFormset(queryset=Flight.objects.get_empty_query_set(),
                    planes_queryset=Plane.objects.user_common(request.display_user))

    return locals()

@no_share('NEVER')
@render_to("mass_entry.html")     
def mass_edit(request, page=0):
    edit = True 
    flights = Flight.objects.filter(user=request.display_user)
    
    try:
        profile = request.display_user.get_profile()
    except:
        profile = Profile()
        
    start = (int(page)-1) * int(profile.per_page)
    duration = int(profile.per_page)
    qs = Flight.objects.filter(user=request.display_user)[start:start+duration]
    NewFlightFormset = modelformset_factory(Flight, form=FormsetFlightForm,
            formset=FixedPlaneModelFormset, extra=0, can_delete=True)
        
    if request.POST.get('submit'):
        formset = NewFlightFormset(request.POST, queryset=qs,
                    planes_queryset=Plane.objects.user_common(request.display_user)
                  )
        
        if formset.is_valid():
            formset.save()
            
            # send signal
            from backup.models import edit_logbook
            edit_logbook.send(sender=request.display_user)
            
            from django.core.urlresolvers import reverse
            return HttpResponseRedirect(
                reverse('logbook-page',
                        kwargs={"username": request.display_user.username,"page": page})
            )
    else:
        formset = NewFlightFormset(queryset=qs,
                    planes_queryset=Plane.objects.user_common(request.display_user),
                  )
    
    return locals()      
