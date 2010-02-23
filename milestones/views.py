from annoying.decorators import render_to
from share.decorator import no_share

@no_share('other')
@render_to('milestones.html')
def milestones(request):
    from logbook.models import Flight
    from calculations import *
    
    u = request.display_user
    
    part135 =   Part135_IFR(u)
    part135v =  Part135_VFR(u)
    atp =       ATP(u)
    private =   Part61_Private(u)
    comm =      Part61_SE_Commercial(u)

    currencies = [private, comm, part135v, part135, atp]
    
    del u   
    
    return locals()

def smallbar(request, val, max_val):
    """
    Returns a small progress bar for use in the milestones app
    """
    
    from small_progress_bar import SmallProgressBar
    return SmallProgressBar(float(val), float(max_val)).as_png()
