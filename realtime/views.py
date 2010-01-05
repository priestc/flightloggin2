import datetime
from annoying.decorators import render_to

@render_to('realtime.html')
def realtime(request):
    from forms import DutyForm
    from models import Duty
    
    # get the current server time to seed the javascript timer
    gmt = datetime.datetime.now() + datetime.timedelta(hours=5)
    
    latest_duty = Duty.latest(user=request.display_user)
    
    if request.POST: #.get('submit') == "Go on Duty":
        form = DutyForm(request.POST, instance=latest_duty)
        if form.is_valid():
            form.save()
    #elif request.POST.get('submit') == "Go off Duty"::

    
    else:
        
        
            
        if latest_duty.on_duty():
            form = DutyForm(instance=latest_duty)
            on_duty = True
        else:
            form = DutyForm()
            on_duty = False
    
    
    
    return locals()
