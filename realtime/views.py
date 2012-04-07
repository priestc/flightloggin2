import datetime
from annoying.decorators import render_to

from main.utils import json_view
from main.utils import ajax_timestamp_to_datetime as atd
from models import Duty, Block

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


def latest_duty_as_json(request):
    """
    Return the latest duty instance and serialize it for display in the page
    """
    
    duty = Duty.latest_open(user=request.display_user)
    
    json = dict(
                    start=duty.start,
                )









###############################################################################



@json_view
def ajax_go_on_duty(request):
    assert request.GET, "Error: no get data"
    ret = {}
    
    #---------

    duty = Duty.latest_open(user=request.display_user) or \
           Duty(user=request.display_user)
           
    duty.start = atd(request.GET['timestamp'])
    duty.save()
    
    #if not duty.latest_open_block():
    #    block = Block(duty=duty)
    #    block.save()
    #    ret['block_id'] = block.id
        
    ret['duty'] = duty.as_json_dict()
    
    return ret
    
    
    
@json_view
def ajax_go_off_duty(request):
    assert request.GET, "Error: no get data"
    duty = Duty.latest_open(user=request.display_user)
    assert duty, "No open Duty"
    ret = {}
    
    #---------
      
    duty.end = atd(request.GET['timestamp'])
    duty.save()
    
    ret['duty'] = duty.as_json_dict()
    
    return ret

#########

@json_view
def ajax_get_master_duty(request):
    """
    Returns a huge json response describing the totality of the latest Duty
    object and all of it's blocks within
    """
    
    duty = Duty.latest_open(user=request.display_user)
    if duty:
        blocks_list = [b.as_json_dict() for b in duty.block_set.all()]
        return {"duty": duty.as_json_dict(), "blocks": blocks_list}
    
    return {'nothing': True}
    

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


