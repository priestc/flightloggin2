from annoying.decorators import render_to
from models import Stat

@render_to('site_stats.html')
def site_stats(request):
    
    ss = Stat()
    ss.get_all()
    
    return locals()
