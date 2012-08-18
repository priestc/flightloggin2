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
    
    @property
    def status_object(self):
        """
        Return the matcing status object that corresponds to the badge this
        instance beongs to.
        """
        for badge in get_badges_classes():
            if self.title == badge.title:
                return badge

    def is_multi_level(self):
        """
        Returns True if this badge is a multilevel badge
        """
        return MultipleLevelBadgeStatus in self.status_object.mro()

    def description(self):
        return self.status_object.get_description(self.level)

    def icon(self):
        """
        Return the icon name that corresponds with the badge.
        """
        if self.level == 1:
            ret = "green"
        elif self.level == 2:
            ret = "blue"
        elif self.level == 3:
            ret = "red"
        elif self.level == 4:
            ret = "purple"
        elif self.level == 5:
            ret = 'gold'

        return "icons/star_%s_48.png" % ret

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

    description = '[placeholder]'

    def __init__(self, new_flight, all_flights=None):
        self.user = new_flight.user
        if all_flights is None:
            self.flights = Flight.objects.filter(user=self.user)
        else:
            self.flights = all_flights
        self.new_flight = new_flight

    @classmethod
    def get_description(cls, level):
        return cls.description

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
            print "badge updated!", self.title, "level", level
        else:
            AwardedBadge.objects.create(
                title=self.title,
                user=self.user,
                awarded_flight=self.new_flight
            )
            print "new badge!!", self.title, " on", self.new_flight.date, "level", level

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
    
    @classmethod
    def get_description(cls, level):
        level_count = getattr(cls, "level_%s" % level)
        description = cls.description % {'level_count': level_count}
        if level < 5:
            # no level after 5
            next_level = getattr(cls, "level_%s" % (level + 1))
            next_level_msg = "Next Level at %s" % next_level
        else:
            next_level_msg = ''
        return "%s (%s)" % (description, next_level_msg)

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
    description = "Your first flight. Congradulations!"
    
    def eligible(self):
        return True


class TwinBadgeStatus(SingleBadgeStatus):
    title = "Twins"
    description = "Logging your first flight in a twin engned aircraft!"

    def eligible(self):
        return self.new_flight.plane.cat_class in (2,4)


class SeaBadgeStatus(SingleBadgeStatus):
    title = "Seaplane"
    description = "Logging your first flight in a seaplane!"

    def eligible(self):
        return self.new_flight.plane.cat_class in (3,4)


class AdaptableBadgeStatus(SingleBadgeStatus):
    title = "Adaptable"
    description = """Logging a flight in a turbine aircraft and a piston aircraft
        on the same day."""

    def eligible(self):
        flights_today = self.flights.filter(date=self.new_flight.date)
        turb = flights_today.turbine().count()
        total = flights_today.count()
        return turb > 0 and total > 0 and turb != total


class TranscontinentalBadgeStatus(SingleBadgeStatus):
    title = "Transcontinental"
    description = "Logging a flight from one continent to another"

    def eligible(self):
        r = self.new_flight.route
        c = Location.objects.filter(routebase__route=r)\
                            .values('country__continent')\
                            .distinct()\
                            .count()
        return c > 2


class CompleteSetBadgeStatus(SingleBadgeStatus):
    title = "Complete Set"
    description = """Logging a flight logged in a single engine, twin engine, 
        tailwheel and a turbine aircraft"""

    def eligible(self):
        planes = Plane.objects.filter(flight__in=self.flights)
        r = {'turbine': False, 'tw': False, 'sea': False, 'single': False, 'multi': False}
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
                r['tw'] = True
        
        return all(r.values())


class ThousandHourBadgeStatus(SingleBadgeStatus):
    title = "One Thousand Hours"
    description = "Logging 1000 hours"

    def eligible(self):
        f = self.flights.aggregate(s=models.Sum('total'))
        c = self.flights.count()
        return f['s'] >= 1000 and c > 100


class FiveThousandHourBadgeStatus(SingleBadgeStatus):
    title = "Five Thousand Hours"
    description = "Logging 5000 hours"

    def eligible(self):
        f = self.flights.aggregate(s=models.Sum('total'))
        c = self.flights.count()
        return f['s'] >= 5000 and c > 500


class TenThousandHourBadgeStatus(SingleBadgeStatus):
    title = "Ten Thousand Hours"
    description = "Logging 10,000 hours"

    def eligible(self):
        f = self.flights.aggregate(s=models.Sum('total'))
        c = self.flights.count()
        return f['s'] >= 10000 and c > 500


class AdventurerBadgeStatus(SingleBadgeStatus):
    title = "Adventurer"
    needed = 25
    description = "Visiting 25 unique airports"
    
    def eligible(self):
        count = Location.objects.filter(routebase__route__flight__in=self.flights)
        return count.count() > self.needed


class NightAdventurerBadgeStatus(SingleBadgeStatus):
    """
    Awarded when the user performs 5 night landings at 5 different airports
    """
    title = "Night Adventurer"
    def eligible(self):
        return False


class PrivateBadgeStatus(SingleBadgeStatus):
    title = "Private Pilot"
    description = "Metting all the requirements for the commercial certificate"
    
    def eligible(self):
        milestone = Part61_Private(user=self.user, as_of_date=self.new_flight.date)
        d = milestone.calculate()
        result = milestone.determine(d)
        for item in result:
            if 'x' in item['icon']:
                return False
        return True


class ATPBadgeStatus(SingleBadgeStatus):
    title = "ATP"
    description = "Meeting all the requirements for the ATP certificate"

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
    title = "Mile High Club"
    description = "Lands at an airport with an elevation of 1 mile"
    
    def eligible(self):
        airport_count = Location.objects\
                                .filter(routebase__route__flight__in=self.flights)\
                                .filter(elevation__gt=5280)\
                                .count()
        
        return airport_count > 1


class ClassBBadgeStatus(MultipleLevelBadgeStatus):
    title = "Class B"
    description = "Landing at %(level_count)s Class B airports"

    level_1 = 1
    level_2 = 5
    level_3 = 10
    level_4 = 20
    level_5 = 35
    
    def eligible(self):
        
        class_b = [
            'KPHX', 'KLAX', 'KNKX', 'KSAN', 'KSFO', 'KDEN', 'KMCO', 'KMIA',
            'KTPA', 'KATL', 'PHNL', 'KORD', 'KCVG', 'KMSY', 'KADW', 'KBWI',
            'KBOS', 'KDTW', 'KMSP', 'KMCI', 'KSTL', 'KLAS', 'KEWR', 'KLGA',
            'KJFK', 'KCLT', 'KCLE', 'KPHL', 'KPIT', 'KMEM', 'KDFW', 'KHOU',
            'KIAH', 'KSLC', 'KDCA', 'KIAD', 'KSEA'
        ]
        count = Location.objects.filter(identifier__in=class_b)\
                                .filter(routebase__route__flight__in=self.flights)\
                                .distinct()\
                                .count()
        
        return self.determine_level(count)


class LongHaulBadgeStatus(MultipleLevelBadgeStatus):
    title = "Long Hauler"
    description = "Logging a flight of %(level_count)s hours in length"

    level_1 = 4
    level_2 = 7
    level_3 = 11
    level_4 = 15
    level_5 = 20

    def eligible(self):
        return self.determine_level(self.new_flight.total) 


class GoingTheDistanceStatus(MultipleLevelBadgeStatus):
    title = "Going the distance"
    description = "Logging a flight with a route of %(level_count)s miles long"

    level_1 = 250
    level_2 = 500
    level_3 = 1000
    level_4 = 2000
    level_5 = 5000

    def eligible(self):
        return self.determine_level(self.new_flight.route.max_width_all)


class WorldExplorerBadgeStatus(MultipleLevelBadgeStatus):
    title = "World Explorer"
    description = "Visiting %(level_count)s different countries"
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
    title = "Busy Bee"
    description = "Visiting %(level_count)s unique airports in the same day"
    
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
        

class TypeMasterBadgeStatus(MultipleLevelBadgeStatus):
    title = "Long Hauler"
    description = "Flying %(level_count)s distinct aircraft types."

    level_1 = 2
    level_2 = 5
    level_3 = 10
    level_4 = 20
    level_5 = 50

    def eligible(self):
        types = self.flight.values_list('plane__type', flat=True).distinct().count()
        return self.determine_level(types)

################################################################################

  
def get_badges_classes():
    return (
        BusyBeeBadgeStatus, WorldExplorerBadgeStatus, FirstFlightBadgeStatus,
        AdaptableBadgeStatus, MileHighClubBadgeStatus, ThousandHourBadgeStatus,
        AdventurerBadgeStatus, ATPBadgeStatus, PrivateBadgeStatus, CompleteSetBadgeStatus,
        FiveThousandHourBadgeStatus, TenThousandHourBadgeStatus, ClassBBadgeStatus,
        TranscontinentalBadgeStatus, GoingTheDistanceStatus, LongHaulBadgeStatus,
        TwinBadgeStatus, TypeMasterBadgeStatus, SeaBadgeStatus
    )

 
def award_badges(new_flight):
    user = new_flight.user
    classes = get_badges_classes()
    for BadgeClass in classes:
        BadgeClass(new_flight).grant_if_eligible()





















