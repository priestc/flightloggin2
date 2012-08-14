from django.http import HttpResponse, HttpResponsePermanentRedirect
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
    return HttpResponse('404')

@render_to('500.html')
def handler500(request):
    return {'shared': False}

@never_cache
def is_alive(request):
    return HttpResponse("OK", mimetype="text/plain")

def robots(request):
    return HttpResponse("""User-agent: *
Disallow: /kml/""", mimetype='text-plain')

def remove_html_redirection(request):
    """
    Dirty hack for dealing with redirecting old urls with the '.html' to the
    nre scheme.
    """
    url = request.path

    if 'logbook' in url or 'graphs' in url:
        _, user, page = url.split('/')
        url = "/%s/%s" % (page, user)
    
    url = url.replace('.html', '')
    print url
    return HttpResponsePermanentRedirect(url)