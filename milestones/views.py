from annoying.decorators import render_to
from share.decorator import no_share

@no_share('other')
@render_to('milestones.html')
def milestones(request):
    from logbook.models import Flight
    from calculations import *
    
    user = request.display_user
    
    part135 =   Part135_IFR(user)
    part135v =  Part135_VFR(user)
    atp =       ATP(user)
    private =   Part61_Private(user)

    currencies = [private, part135v, part135, atp]
        
    
    return locals()

def smallbar(request, val, max_val):
    """
    Returns a small progress bar for use in the milestones app
    """
    
    from small_progress_bar import SmallProgressBar
    return SmallProgressBar(float(val), float(max_val)).as_png()
