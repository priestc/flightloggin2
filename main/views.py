from annoying.decorators import render_to
from annoying.functions import get_object_or_None
from models import NewsItem

@render_to("home.html")
def home(request):
    title = "Home"
    news = NewsItem.objects.all()[:15]
    return locals()

@render_to("preferences.html")
def prefs(request):
    title="Preferences"
    return locals()

@render_to("walkthrough.html")
def help(request):
    title="Walkthrough"
    return locals()

@render_to("faq.html")
def faq(request):
    title="FAQ"
    return locals()

