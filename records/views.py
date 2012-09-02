from annoying.decorators import render_to
from airport.models import Location
from models import Records, NonFlight
from forms import *
from share.decorator import no_share
from backup.models import edit_logbook

@no_share('records')
@render_to("records.html")
def records(request):
      
    if request.POST:
        text = request.POST.get('records', None)
        records = Records(user=request.display_user, text=text)
        records.save()
        saved=True
        
        # send signal to specify this user as editing their data
        edit_logbook.send(sender=request.display_user, touch_cache=False)
    
    else:
        records,c = Records.objects.get_or_create(user=request.display_user)
            
    return locals()

@no_share('logbook')
@render_to("locations.html")
def locations(request):
    customs = Location.objects.user_own(request.display_user)
    changed = False
    
    if "New" in request.POST.get('submit', "DERP"):
        form = CustomForm(request.POST)
        edit_or_new = 'new'
        
        if form.is_valid():
            point = get_point(form.cleaned_data['coordinates'])
            custom = form.save(commit=False)
            custom.loc_class = 3
            custom.location = point
            custom.user = request.display_user
            
            custom.save()
            changed = True
            
        else:
            ERROR = 'true'
            
    elif "Submit" in request.POST.get('submit', "DERP"):
        custom = Location.objects.get(loc_class=3,
                                      user=request.display_user,
                                      pk=request.POST.get('id', None) )
        form = CustomForm(request.POST, instance=custom)
        edit_or_new = 'edit'
        
        if form.is_valid():
            point = get_point(form.cleaned_data['coordinates'])
            custom = form.save(commit=False)
            custom.location = point
            custom.loc_class = 3
            
            custom.save()
            changed = True
            
        else:
            ERROR = 'true'
            
    elif "Delete" in request.POST.get('submit', "DERP"):
        custom = Location.objects.get(loc_class=3,
                                      user=request.display_user,
                                      pk=request.POST.get('id', None)
                                     )
        custom.delete()
        changed = True
        form = CustomForm()
        
    else:
        form = CustomForm()
        
    if changed:
        # send signal to specify this user as editing their data
        edit_logbook.send(sender=request.display_user)
        
    return locals()

@no_share('events')
@render_to("events.html")
def events(request):
    
    profile = request.display_user.get_profile()
        
    if profile.date_format:
        date_format = profile.date_format
    else:
        date_format = "Y-m-d"
    
    ##################################################
    
    nonflights = NonFlight.objects.filter(user=request.display_user).order_by('date')
    changed = False
    
    if request.POST:
        
        if request.POST.get("submit") == "Submit Changes":
            nf = NonFlight(pk=request.POST['id'])
            form = NonFlightForm(request.POST, instance=nf)
            if form.is_valid():
                form.save()
                changed = True
                
        elif request.POST.get("submit") == "Create New Event":
            form = NonFlightForm(request.POST)
            if form.is_valid():
                form.save()
                changed = True
                
        elif request.POST.get("submit") == "Delete Event":
            nf = NonFlight(pk=request.POST.get('id'))
            nf.delete()
            changed = True
            
            form = NonFlightForm()
                
    else:
        form = NonFlightForm(initial={'user': request.user})
        
    if changed:
        # send signal to specify this user as editing their data
        edit_logbook.send(sender=request.display_user, touch_cache=False)
    
    return locals()

def get_point(val):
    """Changes "124.1245521,128.212547" to a Point instance"""
    
    from django.contrib.gis.geos import Point
    
    if not val:
        return None
    
    if not ',' in val:
        return None
    try:    
        x,y = val.split(',')
        point = Point(float(y),float(x))
    except:
        return None
    
    return point
