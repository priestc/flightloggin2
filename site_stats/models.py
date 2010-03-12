import datetime

from django.db import models

from django.contrib.auth.models import User
from django.db.models import Count, Sum, Avg
from logbook.models import Flight
from route.models import RouteBase, Route
from plane.models import Plane
from airport.models import Location

class MostCommonPlane(object):
    title = "??"
    count = "??"
    p = "??"
      
    def __call__(self):
        derp = ""
        for i,item in enumerate(self.p):
            # when the ident is the model, some will have a space, so replace
            # that space with an underscore (for a better URL)
            ident = item[self.title].replace(" ", "_")
            count = item[self.count]
            derp += "%s. %s (%s)\n" % (i+1, ident, count)
        
        return derp

class MostCommonManu(MostCommonPlane):
    title = "manufacturer"
    count = "c"
    
    def __init__(self):
        self.p = Plane.objects\
                      .user('ALL')\
                      .exclude(flight=None)\
                      .exclude(manufacturer='')\
                      .values('manufacturer')\
                      .distinct()\
                      .annotate(c=Count('id'))\
                      .order_by('-c')[:10]

class MostCommonModel(MostCommonPlane):
    title = "model"
    count = "c"
    def __init__(self):
        self.p = Plane.objects\
                      .user('ALL')\
                      .exclude(flight=None)\
                      .exclude(model='')\
                      .values('model')\
                      .distinct()\
                      .annotate(c=Count('id'))\
                      .order_by('-c')[:10]
    
class MostCommonTail(MostCommonPlane):
    title = "tailnumber"
    count = "c"
    def __init__(self):
        self.p = Plane.objects\
                      .user('ALL')\
                      .exclude(flight=None)\
                      .exclude(tailnumber='')\
                      .values('tailnumber')\
                      .distinct()\
                      .annotate(c=Count('id'))\
                      .order_by('-c')[:10]

class StatDB(models.Model):
    dt =               models.DateTimeField()
    
    users =            models.PositiveIntegerField(default=0, null=False)
    non_empty_users =  models.PositiveIntegerField(default=0, null=False)
    
    total_hours =      models.FloatField(default=0, null=False)
    total_logged =     models.PositiveIntegerField(default=0, null=False)
    
    unique_airports =  models.PositiveIntegerField(default=0, null=False)
    unique_countries = models.PositiveIntegerField(default=0, null=False)
    
    total_dist =       models.FloatField(default=0, null=False)
    route_earths =     models.FloatField(default=0, null=False)
    
    avg_per_active =   models.FloatField(default=0, null=False)
    avg_duration =     models.FloatField(default=0, null=False)
    
    most_common_tail = models.TextField()
    most_common_type = models.TextField()
    most_common_manu = models.TextField()
    
    user_7_days =      models.PositiveIntegerField(default=0, null=False)
    num_7_days =       models.PositiveIntegerField(default=0, null=False)
    time_7_days =      models.FloatField(default=0, null=False)
    
    #airport unique visitors
    auv =              models.TextField(null=False)    
    
    pwm_count =        models.PositiveIntegerField(default=0, null=False)
    pwm_hours =        models.FloatField(default=0, null=False)
    
    unique_tn =        models.PositiveIntegerField(default=0, null=False)
    day_wmu =          models.CharField(max_length=25, blank=True, null=True)
    day_wmh =          models.CharField(max_length=25, blank=True, null=True)
    
    class Meta:
        get_latest_by = 'dt'
    
    @classmethod
    def get_object_ago(cls, unit):
        if unit.endswith("d"):
            num = int(unit[:-1])
            dt = datetime.datetime.now() - datetime.timedelta(days=num)
            y=dt.year
            m=dt.month
            d=dt.day
            return cls.objects.filter(dt__year=y, dt__month=m, dt__day=d).latest()
    
    def days_until_million(self):
        """
        Calculate the rate of flights being added by calculating the average
        flights per day based on the past 60 days. The project how long it will
        be until the total there are a million flights.
        """
        
        now = self.total_logged
        sixty = StatDB.get_object_ago('60d').total_logged
        
        rate = float((now - sixty) / 60)
        million_to_go = 1000000 - now
        
        print "now: {now}, sixty_ago: {sixty}, rate: {rate}".format(**locals())
        
        return million_to_go / rate
        
    

class Stat(object):

    def __init__(self):
        
        self.base_flights = Flight.objects.user('ALL')
        
        self.users = User.objects.count()
        self.today = datetime.date.today()
        
        self.sda = datetime.date.today() - datetime.timedelta(days=7)
        
        #all flights in the past 7 days (but not in the future)
        self.fsd = self.base_flights.filter(date__gte=self.sda,
                                            date__lte=self.today)
        
        #person with most...
        self.pwm = User.objects\
                       .exclude(flight=None)\
                       .annotate(s=Sum('flight__total'))\
                       .annotate(c=Count('flight__id'))\
                       .annotate(a=Avg('flight__total'))\
                       .exclude(a__gte=30)
                  
    def save_to_db(self):
        fields = ("users", "non_empty_users", "total_hours", "total_logged",
                  "avg_per_active", "avg_duration", "unique_airports",
                  "unique_countries", "total_dist", "route_earths",
                  "most_common_tail", "most_common_type", "most_common_manu",
                  "auv", "time_7_days", "num_7_days", "user_7_days",
                  "pwm_hours", "pwm_count", "unique_tn", 'day_wmh', 'day_wmu')
          
        kwargs = {"dt": datetime.datetime.now()}
        
        for item in fields:
            kwargs.update({item: getattr(self, "calc_%s" % item).__call__()})
        
        sdb = StatDB(**kwargs)
        sdb.save()
    
    #--------------------------------------------------------------------------
    
    def calc_day_wmh(self):
        """day with the most hours logged, ignoring entries > 24h"""
        item = self.base_flights\
                     .values('total', 'date')\
                     .filter(total__lte=24)\
                     .values('date')\
                     .annotate(t=Sum('total'))\
                     .order_by('-t')[0]
                     
        from django.utils.dateformat import format
        return "%s (%s)" % (format(item['date'], 'd M, Y'), item['t'])
    
    def calc_day_wmu(self):
        """day with most users having edited their logbook"""
        from backup.models import UsersToday
        item = UsersToday.objects\
                         .annotate(c=Count('logged_today'))\
                         .values('c', 'date')\
                         .order_by('-c')[0]
                          
        from django.utils.dateformat import format
                          
        return "%s (%s)" % (format(item['date'], 'd M, Y'), item['c'])
    
    def calc_unique_tn(self):
        return Plane.objects.values('tailnumber').distinct().count()
    
    def calc_pwm_hours(self):
        return self.pwm.order_by('-s').values('s')[:1][0]['s']
    
    def calc_pwm_count(self):
        return self.pwm.order_by('-c').values('c')[:1][0]['c']
        
    def calc_user_7_days(self):
        """
        Number of users who have logged a flight between today and 7 days
        ago, based on the date the flight took place
        """
        
        return User.objects.filter(flight__date__gte=self.sda,
                                   flight__date__lte=self.today)\
                   .values('id')\
                   .distinct()\
                   .count()
    
    def calc_num_7_days(self):
        return self.fsd.count()
    
    def calc_time_7_days(self):
        return self.fsd.exclude(total__gte=24).aggregate(s=Sum('total'))['s'] 
                          
    def calc_auv(self):
        """
        Airport with the most unique visitors
        """
        
        qs = RouteBase.objects\
                      .filter(unknown__isnull=True)\
                      .values('location__identifier')\
                      .annotate(u=Count('route__flight__user', distinct=True))\
                      .order_by('-u')[:10]
        
        foo = ""
        s = "{place}. {ident} ({val})\n"
        for i,item in enumerate(qs):
            ident = item['location__identifier']
            foo += s.format(place=i+1, ident=ident, val=item['u'])
        
        return foo

    # these classes return callable objects
    calc_most_common_manu = MostCommonManu()
    calc_most_common_type = MostCommonModel()
    calc_most_common_tail = MostCommonTail()
    
    def calc_route_earths(self):
        """Must be called after calc_total_dist"""
        EARTH = 21620.6641 #circumference of the earth in NM
        return self.total_dist / EARTH  
    
    def calc_total_dist(self):
        self.total_dist = Route.objects.aggregate(s=Sum('total_line_all'))['s']
        return self.total_dist
    
    def calc_unique_countries(self):
        return RouteBase.objects\
                        .values('location__country')\
                        .distinct()\
                        .count()
    
    def calc_unique_airports(self):
        return RouteBase.objects.values('location').distinct().count()
    
    def calc_avg_duration(self):
        """
        Average length of each flight, excluding adjustment entries
        """
        
        hours = self.base_flights.exclude(total__gte=24).aggregate(t=Sum('total'))['t']
        return hours / self.total_logged
    
    def calc_avg_per_active(self):
        return self.total_hours / self.non_empty_users

    def calc_total_logged(self):
        self.total_logged = self.base_flights.count()
        return self.total_logged

    def calc_total_hours(self):
        self.total_hours = self.base_flights.aggregate(t=Sum('total'))['t']
        return self.total_hours
        
    def calc_non_empty_users(self):
        self.non_empty_users = User.objects\
                        .annotate(f=Count('flight')).filter(f__gte=1).count()
        return self.non_empty_users

    def calc_users(self):
        return self.users




    def openid(self):
        from django_openid_auth.models import UserOpenID
        
        self.google = UserOpenID.objects.filter(claimed_id__contains='google').count()
        self.g_p = self.google / float(self.users) * 100
        
        self.yahoo = UserOpenID.objects.filter(claimed_id__contains='yahoo').count()
        self.y_p = self.yahoo / float(self.users) * 100
        
        self.my = UserOpenID.objects.filter(claimed_id__contains='myopenid').count()
        self.m_p = self.my / float(self.users) * 100
        
        self.aol = UserOpenID.objects.filter(claimed_id__contains='openid.aol').count()
        self.a_p = self.aol / float(self.users) * 100
        
        self.others = self.users - (self.aol + self.my + self.yahoo + self.google)
        self.o_p = self.others / float(self.users) * 100
       
#
# install this crontab to get automatically updated stats
#
# 22 */3 * * * wget http://beta.flightlogg.in/stats_save.py?sk=
