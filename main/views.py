from annoying.decorators import render_to
from models import NewsItem

@render_to("news.html")
def news(request):
    news = NewsItem.objects.all()[:10]
    
    if request.user.is_authenticated():
        request.display_user = request.user
        
    return locals()

def not_found(request):
    from django.http import HttpResponse
    return HttpResponse('404')
