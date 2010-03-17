import datetime

from django.views.decorators.cache import cache_page
from annoying.decorators import render_to

from models import Stat
from share.decorator import secret_key

from utils import *
from constants import STATS_TITLES

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
    
    days_million = cs.days_until_million()
    date_million = datetime.date.today() + datetime.timedelta(days=days_million)
    
    from django.utils.dateformat import format
    date_million = format(date_million, 'd M, Y')
    
    return locals()

@secret_key
def save_to_db(request):

    start = datetime.datetime.now()
    ss = Stat()
    ss.save_to_db()
    stop = datetime.datetime.now()
    
    from django.http import HttpResponse
    return HttpResponse(str(stop-start), mimetype='text/plain')

@cache_page(60 * 60 * 3)
def stats_graph(request, item, ext):
    from graph import StatsGraph, SiteStatsPlot
    
    plots = [SiteStatsPlot(item, no_acc=True)]
    g = StatsGraph(plots, title=item, plot_unit=STATS_TITLES[item][1], rate_unit='rr')
    
    if ext == 'png':
        return g.as_png()
    
    elif ext == 'svg':
        return g.as_svg()
