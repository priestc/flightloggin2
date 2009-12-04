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
            ident = item[self.title]
            count = item[self.count]
            derp += "%s. %s (%s)\n" % (i+1, ident, count)
        
        return derp

class MostCommonManu(MostCommonPlane):
    title = "manufacturer"
    count = "c"
    
    def __init__(self):
        self.p = Plane.objects\
                      .exclude(flight=None)\
                      .exclude(manufacturer='')\
                      .values('manufacturer')\
                      .distinct()\
                      .annotate(c=Count('id'))\
                      .order_by('-c')[:10]

class MostCommonType(MostCommonPlane):
    title = "type"
    count = "c"
    def __init__(self):
        self.p = Plane.objects\
                      .exclude(flight=None)\
                      .exclude(type='')\
                      .values('type')\
                      .distinct()\
                      .annotate(c=Count('id'))\
                      .order_by('-c')[:10]
    
class MostCommonTail(MostCommonPlane):
    title = "tailnumber"
    count = "c"
    def __init__(self):
        self.p = Plane.objects\
                      .exclude(flight=None)\
                      .exclude(tailnumber='')\
                      .values('tailnumber')\
                      .distinct()\
                      .annotate(c=Count('id'))\
                      .order_by('-c')[:10]

class StatDB(models.Model):
    dt = models.DateTimeField()
    
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
    
    pwm_count =        models.PositiveIntegerField(default=0, null=False)
    pwm_hours =        models.FloatField(default=0, null=False)
    
    #airport unique visitors
    auv =              models.TextField(null=False)
    
    class Meta:
        get_latest_by = 'dt'

class Stat(object):

    def __init__(self):
        self.users = User.objects.count()
        self.sda = datetime.date.today() - datetime.timedelta(days=7)
        #all flights in the past 7 days
        self.fsd = Flight.objects.filter(date__gte=self.sda)
        
        #person with most...
        self.pwm = User.objects.exclude(flight=None)\
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
                  "pwm_hours", "pwm_count", )
          
        kwargs = {"dt": datetime.datetime.now()}
        
        for item in fields:
            kwargs.update({item: getattr(self, "calc_%s" % item)()})
        
        sdb = StatDB(**kwargs)
        sdb.save()
    
    #--------------------------------------------------------------------------
    
    def calc_pwm_hours(self):
        return self.pwm.order_by('-s').values('s')[:1][0]['s']
    
    def calc_pwm_count(self):
        return self.pwm.order_by('-c').values('c')[:1][0]['c']
        
    def calc_user_7_days(self):
        return User.objects.filter(flight__date__gte=self.sda)\
                   .distinct().count()
    
    def calc_num_7_days(self):  
        return self.fsd.count()
    
    def calc_time_7_days(self):
        return self.fsd.aggregate(s=Sum('total'))['s'] 
                          
    def calc_auv(self):
        qs = Location.objects\
                     .annotate(u=Count('routebase__route__flight__user',
                               distinct=True))\
                     .order_by('-u')\
                     .values('identifier', 'u')[:10]
        
        foo = ""
        for i,item in enumerate(qs):
            ident = item['identifier']
            count = item['u']
            foo += "%s. %s (%s)\n" % (i+1, ident, count)
        
        return foo
    
    
    calc_most_common_manu = MostCommonManu()
    calc_most_common_type = MostCommonType()
    calc_most_common_tail = MostCommonTail()
    
    def calc_route_earths(self):
        """Must be called after calc_total_dist"""
        EARTH = 21620.6641 #circumference of the earth in NM'
        return self.total_dist / EARTH  
    
    def calc_total_dist(self):
        self.total_dist = Route.objects.aggregate(s=Sum('total_line_all'))['s']
        return self.total_dist
    
    def calc_unique_countries(self):
        return RouteBase.objects\
                        .values('location__country')\
                        .distinct()\
                        .count()

    
    
    def calc_unique_countries(self):
        return RouteBase.objects\
                        .values('location__country')\
                        .distinct()\
                        .count()
    
    def calc_unique_airports(self):
        return RouteBase.objects.values('location').distinct().count()
    
    def calc_avg_duration(self):
        return self.total_hours / self.total_logged
    
    def calc_avg_per_active(self):
        return self.total_hours / self.non_empty_users

    def calc_total_logged(self):
        self.total_logged = Flight.objects.count()
        return self.total_logged

    def calc_total_hours(self):
        self.total_hours = Flight.objects.aggregate(t=Sum('total'))['t']
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
