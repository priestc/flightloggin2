from annoying.decorators import render_to
from models import Stat
from share.decorator import secret_key
from django.core.urlresolvers import reverse

@render_to('site_stats.html')
def site_stats(request):
    
    ss = Stat()
    ss.openid()
    
    from models import StatDB
    cs = StatDB.objects.latest()
    
    tails = cs.most_common_tail.split("\n")
    linked_tail = ""
    for line in tails[:-1]:  ## the last one will be an empty string
        l = line.split(" ")
        tn = l[1]
        url = reverse('profile-tailnumber', kwargs={"tn": tn})
        linked_tail += "%s <a href=\"%s\">%s</a> %s\n" % (l[0], url, tn, l[2])
        
    idents = cs.auv.split("\n")
    linked_airports = ""
    for line in idents[:-1]:
        l = line.split(" ")
        ident = l[1]
        url = reverse('profile-airport', kwargs={"ident": ident})
        linked_airports += "%s <a href=\"%s\">%s</a> %s\n" % (l[0], url, ident, l[2])
    
    types = cs.most_common_type.split("\n")
    linked_mct = ""
    for line in types[:-1]:
        l = line.split(" ")
        ty = l[1]
        url = reverse('profile-type', kwargs={"ty": ty})
        linked_mct += "%s <a href=\"%s\">%s</a> %s\n" % (l[0], url, ty, l[2])
    
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
