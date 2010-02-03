import datetime
from annoying.decorators import render_to
from main.utils import json_view
from models import Duty

@render_to('realtime.html')
def realtime(request):
    from forms import DutyForm
    
    
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





@render_to('realtime.html')
def realtime2(request):

    gmt = datetime.datetime.utcnow()
    duty = Duty.latest_open(user=request.display_user)
    
    return locals()

###############################################################################

from main.utils import ajax_timestamp_to_datetime as atd

@json_view
def ajax_go_on_duty(request):
    assert request.GET, "Error: no get data"
    #assert not Duty.latest_open(user=request.display_user), "Duty already open"
    ret = {}
    
    #---------
    
    start = atd(request.GET['timestamp'])
    
    duty = Duty.latest_open(user=request.display_user) or \
           Duty(user=request.display_user)
           
    duty.start = start

    duty.save()
    
    ret['duty_id'] = duty.id
    
    return ret
    
    
    
@json_view
def ajax_go_off_duty(request):
    assert request.GET, "Error: no get data"
    duty = Duty.latest_open(user=request.display_user)
    assert duty, "No open Duty"
    ret = {}
    
    #---------
    
    end = atd(request.GET['timestamp'])          
    duty.end = end
    duty.save()
    
    ret['duty_id'] = duty.id
    
    return ret

#########

def ajax_new_block(request):
    pass

def ajax_end_block(request):
    pass

#########

def ajax_start_flight(request):
    pass

def ajax_end_flight(request):
    pass

#########

@json_view
def ajax_duty_status(request):
    """
    Returns true of the user has a currently open duty instance
    """
    
    return {"status": bool(Duty.latest_open(user=request.display_user))}


