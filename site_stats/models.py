from django.db import models

from django.contrib.auth.models import User
from django.db.models import Count, Sum
from logbook.models import Flight
from route.models import RouteBase, Route
from plane.models import Plane

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
    
    most_common_tn =   models.CharField(max_length=10)
    most_common_tnc =  models.PositiveIntegerField(default=0, null=False)
    
    most_common_ty =   models.CharField(max_length=10)
    most_common_tyc =  models.PositiveIntegerField(default=0, null=False)
    
    most_common_manu = models.CharField(max_length=10)
    most_common_manuc= models.PositiveIntegerField(default=0, null=False)
    
    class Meta:
        get_latest_by = 'dt'

class Stat(object):    
    
    def save_to_db(self):
        import datetime
        self.get_data()
        
        kwargs = {"dt": datetime.datetime.now()}
        for i in ("users", "non_empty_users", "total_hours", "total_logged",
                  "avg_per_active", "avg_duration", "unique_airports",
                  "unique_countries", "route_earths", "total_dist",
                  "most_common_tn", "most_common_tnc", "most_common_ty",
                  "most_common_tyc", "most_common_manu", "most_common_manuc"):
            kwargs.update({i: getattr(self, i)})
        
        sdb = StatDB(**kwargs)
        sdb.save()
        
    def __init__(self):
        self.users = User.objects.count()

    def get_data(self):
        #return if this function has already been called
        if hasattr(self, "non_empty_users"):
            return
                          
        self.non_empty_users = User.objects\
                              .annotate(f=Count('flight'))\
                              .filter(f__gte=1)\
                              .count()
                              
        self.total_hours =     Flight.objects\
                              .aggregate(t=Sum('total'))['t']
                              
        self.total_logged =    Flight.objects\
                              .count()

        self.unique_airports = RouteBase.objects\
                              .values('location')\
                              .distinct()\
                              .count()
                              
        self.unique_countries = RouteBase.objects\
                              .values('location__country')\
                              .distinct()\
                              .count()
                              
        EARTH = 21620.6641 #circumference of the earth in NM's
        self.total_dist = Route.objects.aggregate(s=Sum('total_line_all'))['s']
        self.route_earths = self.total_dist / EARTH
        
        self.avg_per_active = self.total_hours / self.non_empty_users
        self.avg_duration = self.total_hours / self.total_logged
        
        p = Plane.objects\
                 .exclude(flight=None)\
                 .exclude(tailnumber='')\
                 .values('tailnumber')\
                 .distinct()\
                 .annotate(c=Count('id'))\
                 .order_by('-c')[0]
            
        self.most_common_tn = p['tailnumber']
        self.most_common_tnc = p['c']
                                      
        p = Plane.objects\
                 .exclude(flight=None)\
                 .exclude(type='')\
                 .values('type')\
                 .distinct()\
                 .annotate(c=Count('id'))\
                 .order_by('-c')[0]
                                
        self.most_common_ty = p['type']
        self.most_common_tyc = p['c']     
                                 
        p = Plane.objects\
                 .exclude(flight=None)\
                 .exclude(manufacturer='')\
                 .values('manufacturer')\
                 .distinct()\
                 .annotate(c=Count('id'))\
                 .order_by('-c')[0]
                                
        self.most_common_manu = p['manufacturer']
        self.most_common_manuc = p['c']
        
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
        
