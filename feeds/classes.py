from django.contrib.syndication.feeds import Feed
from logbook.models import Flight
from main.models import NewsItem

from django.contrib.syndication.feeds import FeedDoesNotExist
from django.core.exceptions import ObjectDoesNotExist

from django.contrib.auth.models import User

class LatestFlights(Feed):
    
    def get_object(self, bits):
        if len(bits) != 1:
            raise ObjectDoesNotExist
        user=User.objects.get(username=bits[0])
        
        try:
            if not user.get_profile().logbook_share:
                raise ObjectDoesNotExist 
        except:
            raise ObjectDoesNotExist
        
        return user

    def title(self, user):
        return "%s's FlightLogg.in' Logbook feed" % user.username
    
    def link(self, user):
        if not user:
            raise FeedDoesNotExist
        return user.get_profile().get_absolute_url()
    
    def description(self, user):
        return "Latest flights logged by %s" % user.username

    def items(self, user):
        return Flight.objects.user(user).order_by('-date')[:15]

class LatestNews(Feed):
    title = "FlightLogg.in News"
    link = "http://flightlogg.in"
    description = "Latest news items from http://flightlogg.in"

    def items(self):
        return NewsItem.objects.order_by('-date')[:5]

    def item_title(self, item):
        return "%s - %s" % (item.date, item.title)

    def item_description(self, item):
        return item.text
    
    def item_link(self):
        return "http://flightlogg.in/news.html"

