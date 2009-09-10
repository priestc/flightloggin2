from annoying.decorators import render_to
from annoying.functions import get_object_or_None
from models import Records
from forms import *
from is_shared import is_shared

@render_to("records.html")
def records(request, username):
    shared, display_user = is_shared(request, username)
    
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
    
    records,c = Records.objects.get_or_create(user=request.user)
    
    nonflights = NonFlight.objects.filter(user=request.user)
    
    if request.POST:
        
        if request.POST.get("submit") == "Edit Event":
            nf = NonFlight(pk=request.POST['id'])
            form=NonFlightForm(request.POST, instance=nf)
            if form.is_valid():
                form.save()
                
        elif request.POST.get("submit") == "New Event":
            form=NonFlightForm(request.POST)
            if form.is_valid():
                form.save()
                
        #records.text=request.POST.get('records')
        #records.save()
        #saved=True

    else:
        form = NonFlightForm()
    
    return locals()
