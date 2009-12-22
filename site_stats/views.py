from annoying.decorators import render_to
from models import Stat
from share.decorator import secret_key

@render_to('site_stats.html')
def site_stats(request):
    
    ss = Stat()
    ss.openid()
    
    from models import StatDB
    cs = StatDB.objects.latest()

    return locals()

@secret_key
def save_to_db(request):
    import datetime
    start = datetime.datetime.now()
    ss = Stat()
    ss.save_to_db()
    stop = datetime.datetime.now()
    
    from django.http import HttpResponse
    return HttpResponse(str(stop-start), mimetype='text/plain')
