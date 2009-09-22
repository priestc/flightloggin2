from django.contrib.syndication.feeds import Feed
from logbook.models import Flight

from django.contrib.syndication.feeds import FeedDoesNotExist
from django.core.exceptions import ObjectDoesNotExist

from django.contrib.auth.models import User

class LatestFlights(Feed):
    
    def get_object(self, bits):
        if len(bits) != 1:
            raise ObjectDoesNotExist
        return User.objects.get(username=bits[0])

    def title(self, user):
        return "%s's FlightLogg.in' Logbook feed" % user.username
    
    def link(self, user):
        if not user:
            raise FeedDoesNotExist
        return user.get_profile().get_absolute_url()
    
    def description(self, user):
        return "Latest flights logged by %s" % user.username

    def items(self, user):
        return Flight.objects.filter(user=user).order_by('-date')[:15]

