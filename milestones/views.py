from annoying.decorators import render_to
from share.decorator import no_share

@no_share('other')
@render_to('milestones.html')
def milestones(request):
    from logbook.models import Flight
    from calculations import *
    
    qs = Flight.objects.user(request.display_user)
    
    part135 = part135ifr(qs)
    part135v = part135vfr(qs)
    atp = atp_calc(qs)
    private = p61_private(qs)
    
    dual60 = figure_dual60(qs)
        
    
    return locals()

def smallbar(request, val, max_val):
    """
    Returns a small progress bar for use in the milestones app
    """
    
    from small_progress_bar import SmallProgressBar
    return SmallProgressBar(float(val), float(max_val)).as_png()
