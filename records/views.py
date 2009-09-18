from annoying.decorators import render_to
from annoying.functions import get_object_or_None
from airport.models import Custom
from models import Records, NonFlight
from forms import *

@render_to("places.html")
def places(request, shared, display_user):
    customs = Custom.objects.filter(user=display_user)
    
    if request.POST.get('submit', None) == 'Create New Place':
        form=CustomForm(request.POST)
        if form.is_valid():
            point = get_point(form.cleaned_data['coordinates'])
            custom = form.save()
            custom.location = point
            custom.save()
            
        else:
            assert False, form.errors
            ERROR = 'true'
            
    elif request.POST.get('submit', None) == 'Submit Changes':
        custom = Custom.objects.get(user=display_user, pk=request.POST.get('id', None) )
        form=CustomForm(request.POST, instance=custom)
        if form.is_valid():
            point = get_point(form.cleaned_data['coordinates'])
            custom = form.save()
            custom.location = point
            custom.save()
        else:
            ERROR = 'true'
            
    elif request.POST.get('submit', None) == 'Delete Place':
        custom = Custom.objects.get(user=display_user, pk=request.POST.get('id', None) )
        custom.delete()
        form = CustomForm()
        
    else:
        form = CustomForm()
        
    return locals()

@render_to("records.html")
def records(request, shared, display_user):
    
    ##################################################

    try:
        profile = display_user.get_profile()
    except:
        profile = Profile()
        
    if profile.date_format:
        date_format = profile.date_format
    else:
        date_format = "Y-m-d"
    
    ##################################################
    
    records,c = Records.objects.get_or_create(user=display_user)
    
    nonflights = NonFlight.objects.filter(user=display_user).order_by('date')
    
    if request.POST:
        
        if request.POST.get("submit") == "Submit Changes":
            nf = NonFlight(pk=request.POST['id'])
            form=NonFlightForm(request.POST, instance=nf)
            if form.is_valid():
                form.save()
                
        elif request.POST.get("submit") == "Create New Event":
            form=NonFlightForm(request.POST)
            if form.is_valid():
                form.save()
                
    else:
        form = NonFlightForm()
    
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
