from django.db import models
from airport.models import Location
from logbook.models import Flight
from plane.models import Plane
from milestones.calculations import Part61_Private, ATP

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
    
    @classmethod
    def total_badge_count(cls, user):
        """
        Count of badges that the user has been awarded.
        """
        return cls.objects.filter(user=user).aggregate(s=models.Sum('level'))['s']
    
    def award(status_class):
        """
        Award the user ith this badge.
        status_class is one of the clases in this file that that ends with
        StatusClass.
        """
        self.user = status_class.user
        self.title = status_class.title
        self.awarded_flight = status_class.new_flight
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

class TwinBadgeStatus(SingleBadgeStatus):
    """
    Awarded when a User logs his first flight in a twin
    """
    title = "Twins"

    def eligible(self):
        return self.new_flight.plane.cat_class in (2,4)

class AdaptableBadgeStatus(SingleBadgeStatus):
    """
    Awarded when a user logs a flight in a turbine aircraft and a piston
    aircraft in the same day.
    """
    title = "Adaptable"
    
    def eligible(self):
        flights_today = self.flights.filter(date=self.new_flight.date)
        return flights_today.turbine().count() - flights_today.count() != 0

class CompleteSetBadgeStatus(SingleBadgeStatus):
    """
    Awarded when you have a flight logged in a single engine, twin engine,
    tailwheel and a turbine aircraft
    """
    title = "Complete Set"
    
    def eligible(self):
        planes = Plane.objects.filter(flight__in=self.flights)
        r = {'turbine': False, 'tailwheel': False, 'sea': False, 'single': False, 'multi': False}
        for p in planes:
            if p.cat_class in [2,4]:
                r['multi'] = True
            if p.cat_class in [1,3]:
                r['single'] = True
            if p.cat_class in [3,4]:
                r['sea'] = True
            if 'turbine' in p.tags.lower():
                r['turbine'] = True
            if 'tailwheel' in p.tags.lower():
                r['tailwheel'] = True
        
        return all(r.values())

class ThousandHourBadgeStatus(SingleBadgeStatus):
    """
    Awarded when the user logs 1000 hours.
    """
    title = "One Thousand Hours"
    
    def eligible(self):
        f = self.flights.aggregate(s=models.Sum('total'))
        c = self.flights.count()
        return f['s'] >= 1000 and c > 100

class FiveThousandHourBadgeStatus(SingleBadgeStatus):
    """
    Awarded when the user logs 5000 hours.
    """
    title = "Five Thousand Hours"

    def eligible(self):
        f = self.flights.aggregate(s=models.Sum('total'))
        c = self.flights.count()
        return f['s'] >= 5000 and c > 500

class TenThousandHourBadgeStatus(SingleBadgeStatus):
    """
    Awarded when the user logs 5000 hours.
    """
    title = "Ten Thousand Hours"

    def eligible(self):
        f = self.flights.aggregate(s=models.Sum('total'))
        c = self.flights.count()
        return f['s'] >= 10000 and c > 500

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
        milestone = Part61_Private(user=self.user, as_of_date=self.new_flight.date)
        d = milestone.calculate()
        result = milestone.determine(d)
        for item in result:
            if 'x' in item['icon']:
                return False
        return True


class ATPBadgeStatus(SingleBadgeStatus):
    """
    Awarded when the user gets all the requirements for the FAA Private license
    """
    title = "ATP"

    def eligible(self):
        milestone = ATP(user=self.user, as_of_date=self.new_flight.date)
        d = milestone.calculate()
        result = milestone.determine(d)
        for item in result:
            if 'x' in item['icon']:
                return False
        return True

################################################################################

class MileHighClubBadgeStatus(SingleBadgeStatus):
    """
    Awarded when a user lands at an airport with an elevation 1 mile MSL
    """
    title = "Mile High Club"
    
    def eligible(self):
        airport_count = Location.objects\
                                .filter(routebase__route__flight__in=self.flights)\
                                .filter(elevation__gt=5280)\
                                .count()
        
        return airport_count > 1

   
class ClassBBadgeStatus(MultipleLevelBadgeStatus):
    """
    Awarded when the user lands at a large airport.
    """
    title = "Class B"
    
    level_1 = 1
    level_2 = 5
    level_3 = 10
    level_4 = 20
    level_5 = 35
    
    def eligible(self):
        airports = Location.objects.filter(routebase__route__flight__in=self.flights)\
                                   .values_list('identifier', flat=True)\
                                   .distinct()
        class_b = [
            'KPHX', 'KLAX', 'KNKX', 'KSAN', 'KSFO', 'KDEN', 'KMCO', 'KMIA',
            'KTPA', 'KATL', 'PHNL', 'KORD', 'KCVG', 'KMSY', 'KADW', 'KBWI',
            'KBOS', 'KDTW', 'KMSP', 'KMCI', 'KSTL', 'KLAS', 'KEWR', 'KLGA',
            'KJFK', 'KCLT', 'KCLE', 'KPHL', 'KPIT', 'KMEM', 'KDFW', 'KHOU',
            'KIAH', 'KSLC', 'KDCA', 'KIAD', 'KSEA'
        ]
        count = 0
        for a in class_b:
            if a in airports:
                count +=1
        
        return self.determine_level(count)
    
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
    return (
        BusyBeeBadgeStatus, WorldExplorerBadgeStatus, FirstFlightBadgeStatus,
        AdaptableBadgeStatus, MileHighClubBadgeStatus, ThousandHourBadgeStatus,
        AdventurerBadgeStatus, ATPBadgeStatus, PrivateBadgeStatus, CompleteSetBadgeStatus,
        FiveThousandHourBadgeStatus, TenThousandHourBadgeStatus, ClassBBadgeStatus,
        
    )

 
def award_badges(new_flight):
    user = new_flight.user
    classes = get_badges_classes()
    for BadgeClass in classes:
        BadgeClass(new_flight).grant_if_eligible()





















