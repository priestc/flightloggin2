from django.http import HttpResponse
from django.views.decorators.cache import never_cache

from annoying.decorators import render_to
from models import NewsItem, HelpItem

@render_to("news.html")
def news(request):
    news = NewsItem.objects.all()[:10]

    if request.user.is_authenticated():
        request.display_user = request.user
        
    return locals()


@render_to("help.html")
def help(request):
    
    helpitems = HelpItem.objects.order_by('category', 'order', 'id')
    
    return locals()

def not_found(request):
    from django.http import HttpResponse
    return HttpResponse('404')

@render_to('500.html')
def handler500(request):
    return {'shared': False}

@never_cache
def is_alive(request):
    return HttpResponse("OK", mimetype="text/plain")

def robots(request):
    return HttpResponse("""User-agent: *
Disallow: *.kmz""", mimetype='text-plain')
