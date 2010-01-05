import datetime
from annoying.decorators import render_to

@render_to('realtime.html')
def realtime(request):
    from forms import DutyForm
    from models import Duty
    
    # get the current server time to seed the javascript timer
    gmt = datetime.datetime.now() + datetime.timedelta(hours=5)
    
    latest_open_duty = Duty.latest_open(user=request.display_user)
    
    if request.POST: #.get('submit') == "Go on Duty":
        form = DutyForm(request.POST, instance=latest_open_duty)
        if form.is_valid():
            form.save()
        
        print request.POST.get('submit')
        
        if request.POST.get('submit') == "Go On Duty":
            on_duty = True
        
        if request.POST.get('submit') == "Go Off Duty":
            on_duty = False
            form = DutyForm()
    else:

        if latest_open_duty.on_duty():
            form = DutyForm(instance=latest_open_duty)
            on_duty = True
            
        else:
            form = DutyForm()
            on_duty = False
    
    
    
    return locals()
