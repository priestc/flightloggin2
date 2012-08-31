from django.http import HttpResponse, HttpResponsePermanentRedirect
from django.views.decorators.cache import never_cache
from django.core.urlresolvers import reverse

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
    new scheme.
    """
    url = request.path

    if 'logbook' in url or 'graphs' in url:
        _, user, page = url.split('/')
        url = "/%s/%s" % (page, user)
    
    url = url.replace('.html', '')
    return HttpResponsePermanentRedirect(url)

def temp_redirect(request, ident):
    """
    Urls for the various profile pages have changed, so instead of all old links
    ending up as 404s, return a 301 redirect. After some time, this redirect can be removed
    """
    for item in ('location', 'navaid', 'airport', 'route', 'tailnumber', 'type', 'model'):
        if item in request.path:
            url = reverse('profile-%s' % item, args=(ident,))
            return HttpResponsePermanentRedirect(url)