from annoying.decorators import render_to
from annoying.functions import get_object_or_None
from models import Records
from forms import *

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
