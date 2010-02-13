from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.forms.models import modelformset_factory
from django.forms.formsets import formset_factory
from django.core.urlresolvers import reverse
    
from annoying.decorators import render_to
from share.decorator import no_share

from models import Flight, Columns
from plane.models import Plane
import forms
from constants import *
from profile.models import Profile, AutoButton

from utils import proper_flight_form, logbook_url, expire_page

from django.views.decorators.cache import cache_page

###############################################################################

def root_logbook(request):
    """
    Find the last page in the user's logbook, then redirect to that page
    
    """
    
    from django.core.urlresolvers import reverse
    import math
    
    try:
        per_page = request.display_user.get_profile().per_page
    except:
        per_page = 50
    
    flights = Flight.objects.user(request.display_user).count()
    last_page = int(math.ceil(flights / float(per_page)))
    
    url = reverse("logbook-page", kwargs={"page": last_page,
                                          "username": request.display_user})
    
    return HttpResponseRedirect(url)

###############################################################################

def delete_flight(request, page):
    url = logbook_url(request.display_user, page)
    
    if not request.POST:
        return HttpResponseRedirect(url)
        
    if request.display_user.username != 'ALL':
        flight_id = request.POST['id']
        Flight(pk=flight_id, user=request.display_user).delete()
        
        from backup.models import edit_logbook
        edit_logbook.send(sender=request.display_user)
    
    return HttpResponseRedirect(url)

###############################################################################

def edit_flight(request, page):

    if not request.POST:
        return HttpResponseRedirect(url)
    
    profile,c = Profile.objects.get_or_create(user=request.display_user)
    PopupFlightForm = proper_flight_form(profile)
    
    flight_id = request.POST['id']
    flight = Flight(pk=flight_id, user=request.display_user)

    form = PopupFlightForm(request.POST,
                           user=request.display_user,
                           instance=flight,
                           prefix="new")

    if form.is_valid() and request.display_user.username != 'ALL':
        form.save()
        
        from backup.models import edit_logbook
        edit_logbook.send(sender=request.display_user)
        
        url = logbook_url(request.display_user, page)
        return HttpResponseRedirect(url)
        
    return logbook(request, form=form, fail="edit")
    
###############################################################################

def new_flight(request, page):
    if not request.POST:
        url = logbook_url(request.display_user, page)
        return HttpResponseRedirect(url)
    
    profile,c = Profile.objects.get_or_create(user=request.display_user)
    PopupFlightForm = proper_flight_form(profile)

    flight = Flight(user=request.display_user)
    
    form = PopupFlightForm(request.POST,
                           user=request.display_user,
                           instance=flight,
                           prefix="new")
    
    if form.is_valid() and request.display_user.username != 'ALL':
        form.save()
        
        from backup.models import edit_logbook
        edit_logbook.send(sender=request.display_user)
        
        url = logbook_url(request.display_user, page)
        return HttpResponseRedirect(url)

    return logbook(request, form=form, fail="new")
    
###############################################################################

@cache_page(60 * 60 * 24)
@render_to("logbook.html")
@no_share('logbook')
def logbook(request, page, form=None, fail=None):
    """
    Prepare the Logbook page
    """
    
    if page == "0":
        url = reverse("logbook", kwargs={"username": request.display_user})
        return HttpResponseRedirect(url)
    
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
    
    all_flights = Flight.objects\
                        .user(request.display_user, disable_future=True)\
                        .order_by('date', 'id')
                        
    filtered_flights = all_flights.select_related()
    total_sign = "Overall"
    
    if request.GET:
        ff=FilterForm(request.GET)
        filtered_flights = filtered_flights.custom_logbook_view(ff)
        ## split it to get just the part after the '?', ignore the part before
        get = "?" + request.get_full_path().split("?")[1]
        total_sign = "Filter"
            
    ############## google maps and google earth filter below ################
    
    earth = request.GET.get('earth')
    maps = request.GET.get('maps')
    
    if earth == 'true':
        from maps.utils import qs_to_time_kmz
        from route.models import Route
        routes = Route.objects.filter(flight__in=filtered_flights)
        response = qs_to_time_kmz(routes)
        response['Content-Disposition'] = 'attachment; filename=filter.kmz'
        return response
    
    if maps == 'true':
        url = "http://maps.google.com/?q=http://flightlogg.in/%s/logbook.html%s"
        get = get.replace('maps=true', "earth=true").replace('&', '%26')
        return HttpResponseRedirect(url % (request.display_user.username, get))

    
    ############### pagination stuff below ############################
    
    before_block, after_block, page_of_flights = \
                   Flight.make_pagination(filtered_flights, profile, int(page))
    
    #only make the page table if there are more than one pages overall
    do_pagination = page_of_flights.paginator.num_pages > 1
    
    if not form:
        PopupFlightForm = proper_flight_form(profile)
        form = PopupFlightForm(prefix="new")
    else:
        ## set this variable so we know which popup to prepare to enter the
        ## failed form data
        edit_or_new = fail
        
    return locals()

###############################################################################
###############################################################################
###############################################################################
###############################################################################
###############################################################################

@no_share('NEVER')
@render_to("mass_entry.html")     
def mass_entry(request):
    
    profile,c = Profile.objects.get_or_create(user=request.display_user)
        
    NewFlightFormset = modelformset_factory(Flight,
                                       form=forms.FormsetFlightForm,
                                       extra=profile.per_page,
                                       formset=forms.FixedPlaneModelFormset)
        
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
                    planes_queryset=Plane.objects.user_common(request.display_user)
                  )
        
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
        qs = Flight.objects.get_empty_query_set()
        pqs = Plane.objects.user_common(request.display_user)
        formset = NewFlightFormset(queryset=qs, planes_queryset=pqs)

    return locals()

@no_share('NEVER')
@render_to("mass_entry.html")     
def mass_edit(request, page=0):
    edit = True 
    flights = Flight.objects.filter(user=request.display_user)
    profile,c = Profile.objects.get_or_create(user=request.display_user)
        
    start = (int(page)-1) * int(profile.per_page)
    duration = int(profile.per_page)
    qs = Flight.objects.filter(user=request.display_user)\
                       .order_by('date')[start:start+duration]
    
    NewFlightFormset = modelformset_factory(Flight,
                                            form=forms.FormsetFlightForm,
                                            formset=forms.FixedPlaneModelFormset,
                                            extra=0,
                                            can_delete=True)
        
    if request.POST.get('submit'):
        formset = NewFlightFormset(request.POST, queryset=qs,
                    user=request.display_user,
                    planes_queryset=Plane.objects.user_common(request.display_user)
                  )
        
        if formset.is_valid():
            formset.save()
            
            ## send signal to mark this user as having
            ## edited their logbook for today
            from backup.models import edit_logbook
            edit_logbook.send(sender=request.display_user)
            
            from django.core.urlresolvers import reverse
            return HttpResponseRedirect(
                reverse('logbook-page',
                        kwargs={"username": request.display_user.username,
                                "page": page})
            )
    else:
        pqs = Plane.objects.user_common(request.display_user)
        formset = NewFlightFormset(queryset=qs, planes_queryset=pqs)
    
    return locals()      
