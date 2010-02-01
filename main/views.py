from annoying.decorators import render_to
from models import NewsItem

@render_to("news.html")
def news(request):
    news = NewsItem.objects.all()[:15]
    
    if request.user.is_authenticated():
        request.display_user = request.user
        
    return locals()

@render_to("faq.html")
def faq(request):
    title="FAQ"
    return locals()
    
@render_to("help.html")
def help(request):
    title="Help"
    return locals()

def not_found(request):
    from django.http import HttpResponse
    return HttpResponse('404')

def login_wrapper(request):
    from django.http import HttpResponseRedirect
    from django.core.urlresolvers import reverse
    
    ua = request.META['HTTP_USER_AGENT']
    
    if ("MSIE 7.0" in ua) or ("MSIE 6.0" in ua):
        url = reverse('basic-login')
    else:
        url = reverse('fancy-login')    
        
    return HttpResponseRedirect(url)
