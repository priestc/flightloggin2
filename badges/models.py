from django.db import models
from airport.models import Location
from logbook.models import Flight

class AwardedBadge(models.Model):
    user = models.ForeignKey('auth.User')
    awarded_date = models.DateTimeField(auto_now=True)
    awarded_flight = models.ForeignKey('logbook.Flight')
    title = models.CharField(max_length=64)
    level = models.IntegerField(default=1)
    
    def __unicode__(self):
        return "%s %s(%s) - %s - %s" % (
            self.id, self.title, self.level, self.user.username, self.awarded_flight
        )
    
    def award(status_class, awarding_flight):
        """
        Award the user ith this badge.
        status_class is one of the clases in this file that that ends with
        StatusClass.
        """
        self.user = user
        self.title = status.title
        self.awarded_flight = awarding_flight
        self.save()

#################################

class BadgeStatus(object):
    def __init__(self, new_flight, all_flights=None):
        self.user = new_flight.user
        if all_flights is None:
            self.flights = Flight.objects.filter(user=self.user)
        else:
            self.flights = all_flights
        self.new_flight = new_flight

    def grant_badge(self, level=1):
        badge = AwardedBadge.objects.filter(
            title=self.title,
            user=self.user
        )
        
        if badge:
            badge = badge[0]
            badge.awarded_flight=self.new_flight
            badge.level = level
            badge.save()
            print "badge updated! level", level
        else:
            AwardedBadge.objects.create(
                title=self.title,
                user=self.user,
                awarded_flight=self.new_flight
            )
            print "new badge!! on", self.new_flight.date, "level", level

class SingleBadgeStatus(BadgeStatus):
    
    def already_awarded(self):
        return AwardedBadge.objects.filter(user=self.new_flight.user, title=self.title).exists()
    
    def grant_if_eligible(self):
        if self.already_awarded():
            return False
        if self.eligible():
            self.grant_badge()

class MultipleLevelBadgeStatus(BadgeStatus):
    """
    A badge that can be awarded multiple times. Each time at a different level.
    """
    
    # defaults (can be overridden)
    level_1 = 1
    level_2 = 5
    level_3 = 10
    level_4 = 25
    level_5 = 50
    
    def determine_level(self, count):        
        if count >= self.level_5:
            return 5
        if count >= self.level_4:
            return 4
        if count >= self.level_3:
            return 3
        if count >= self.level_2:
            return 2
        if count >= self.level_1:
            return 1
        
        return 0
    
    def current_level(self):
        badge = AwardedBadge.objects.filter(user=self.new_flight.user, title=self.title)
        current_level = 0
        if badge:
            current_level = badge[0].level
        return current_level
    
    def grant_if_eligible(self):
        level = self.eligible()
        if level == 0:
            return
        
        if level > self.current_level():
            self.grant_badge(level=level)
        

################################################################################

class FirstFlightBadgeStatus(SingleBadgeStatus):
    """
    Awarded when a User logs his first flight
    """
    title = "First Flight"
    
    def eligible(self):
        return True

class AdaptableBadgeStatus(SingleBadgeStatus):
    """
    Awarded when a user logs a flight in a turbine aircraft and a piston
    aircraft in the same day.
    """
    title = "Adaptable"
    
    def eligible(self):
        flights_today = self.flights.filter(date=self.new_flight.date)
        return flights_today.turbine().count() - flights_today.count() != 0

class ThousandHourBadgeStatus(SingleBadgeStatus):
    """
    Awarded when the user logs 1000 hours.
    """
    title = "One Thousand Hours"
    
    def eligible(self):
        f = self.flights.aggregate(s=models.Sum('total'))
        return f['s'] >= 1000

class AdventurerBadgeStatus(SingleBadgeStatus):
    """
    Awarded when the user visits more than 25 airports
    """
    title = "Adventurer"
    needed = 25
    
    def eligible(self):
        count = Location.objects.filter(routebase__route__flight__in=self.flights)
        return count > self.needed

class NightAdventurerBadgeStatus(SingleBadgeStatus):
    """
    Awarded when the user performs 5 night landings at 5 different airports
    """
    title = "Night Adventurer"
    def eligible(self):
        return False

class PrivateBadgeStatus(SingleBadgeStatus):
    """
    Awarded when the user gets all the requirements for the FAA Private license
    """
    title = "Private Pilot"
    def eligible(self):
        return False

################################################################################

class MileHighClubBadgeStatus(MultipleLevelBadgeStatus):
    """
    Awarded when a user lands at an airport with an elevation 1 mile MSL
    """
    title = "Mile High Club"
    
    def eligible(self):
        airport_count = Location.objects\
                                .filter(routebase__route__flight__in=self.flights)\
                                .filter(elevation__gt=5280)\
                                .count()
        
        return self.determine_level(airport_count)

   
class RidingWithTheBigBoysBadgeStatus(MultipleLevelBadgeStatus):
    """
    Awarded when the user lands at a large airport.
    """
    title = "Riding With The Big Boys"
    def eligible(self):
        ret = self.new_flight.route.routebase_set.filter(location__loc_class=3).exists()
        print ret
        return ret
    
class LongHaulBadgeStatus(MultipleLevelBadgeStatus):
    """
    Awarded when a user logs enough long (in terms of distance) flights.
    """
    title = "Long Hauler"
    def eligible(self):
        return False
    
class WorldExplorerBadgeStatus(MultipleLevelBadgeStatus):
    """
    Awarded when the user lands in a diferent country.
    """
    title = "World Explorer"
    level_1 = 2
    
    def eligible(self):
        countries = Location.objects\
                            .filter(routebase__route__flight__in=self.flights)\
                            .values('country')\
                            .distinct()
        c = countries.count()
        level = self.determine_level(c)
        return level

class BusyBeeBadgeStatus(MultipleLevelBadgeStatus):
    """
    Landing at multiple airports in a single day.
    """
    title = "Busy Bee"
    
    level_1 = 4
    level_2 = 6
    level_3 = 10
    level_4 = 14
    level_5 = 20
    
    def eligible(self):
        date = self.new_flight.date
        count = Location.objects\
                        .filter(
                            routebase__route__flight__user=self.user,
                            routebase__route__flight__date=date
                         )\
                        .distinct()\
                        .count()
        return self.determine_level(count)
        

################################################################################

  
def get_badges_classes():
    classes = globals()
    ret = []
    for name, class_ in classes.iteritems():
        if not hasattr(class_, 'mro'):
            continue
        if BadgeStatus in class_.mro() and class_ not in [MultipleLevelBadgeStatus, BadgeStatus, SingleBadgeStatus]:
            ret.append(class_)
    return ret

 
def award_badges(new_flight):
    user = new_flight.user
    classes = get_badges_classes()
    for BadgeClass in classes:
        BadgeClass(new_flight).grant_if_eligible()





















