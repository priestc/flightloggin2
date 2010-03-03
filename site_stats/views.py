from django.views.decorators.cache import cache_page
from annoying.decorators import render_to
from models import Stat
from share.decorator import secret_key
from django.core.urlresolvers import reverse

def link_airports(lines):
    from airport.models import Location
    
    tem = '{number} <a title="{title}" href="{url}">{ident}</a> {value}\n'
    
    out = ""
    for line in lines[:-1]:
        s = line.split(" ")
        ident = s[1]
        
        title = Location.objects\
                        .get(identifier=ident, loc_class=1)\
                        .location_summary()
                        
        url = reverse('profile-airport', kwargs={"ident": ident})

        out += tem.format(number=s[0],
                         title=title,
                         url=url,
                         ident=ident,
                         value=s[2])
    
    return out

def link_tails(lines):
    
    tem = '{number} <a href="{url}">{tail}</a> {value}\n'
    
    out = ""
    for line in lines[:-1]:  ## the last one will be an empty string
        s = line.split(" ")
        tn = s[1]
        url = reverse('profile-tailnumber', kwargs={"tn": tn})
        out += tem.format(number=s[0], url=url, tail=tn, value=s[2])
        
    return out

def link_models(lines):
    
    tem = '{number} <a href="{url}">{model}</a> {value}\n'
    
    out = ""
    for line in lines[:-1]:
        s = line.split(" ")
        model = s[1]
        url = reverse('profile-model', kwargs={"model": model})
        # put the space back in instead of the underscore
        model = model.replace('_', ' ')
        out += tem.format(number=s[0], url=url, model=model, value=s[2])
    
    return out

@render_to('site_stats.html')
def site_stats(request):
    
    ss = Stat()
    ss.openid()
    
    from constants import STATS_TITLES as t
    
    from models import StatDB
    cs = StatDB.objects.latest()
    
    tails = cs.most_common_tail.split("\n")
    linked_tail = link_tails(tails)
        
    idents = cs.auv.split("\n")
    linked_airports = link_airports(idents)
    
    models = cs.most_common_type.split("\n")
    linked_mct = link_models(models)
    
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

@cache_page(60 * 60 * 3)
def stats_graph(request, item, ext):
    from graph import StatsGraph
    
    try:
        g = StatsGraph(item)
    except Exception, e:
        from django.http import Http404
        raise Http404(e)
    
    if ext == 'png':
        return g.as_png()
    
    elif ext == 'svg':
        return g.as_svg()
