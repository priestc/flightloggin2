from django.db.models import Q
from django.db.models.query import QuerySet
from django.db.models import Sum

from constants import *

class LogbookRow(list):
    date = ""
    plane = ""
    pk = 0

def to_minutes(flt):
    """converts decimal to HH:MM
    
    >>> to_minutes(.5452)
    '0:33'
    >>> to_minutes(2)
    2:00
    >>> to_minutes(1.2)
    '1:12'
    >>> to_minutes(-1.2)
    '-1:12'
    """
    
    value = str(flt + 0.0)
    h,d = value.split(".")
    minutes = float("0." + d) * 60
    return str(h) + ":" + "%02.f" % minutes
    
def from_minutes(value):
    """converts HH:MM to decimal
    
    >>> from_minutes("1:45")
    1.75
    >>> from_minutes("1:75")
    2.25
    >>> from_minutes("0:17")
    0.28333333333333333
    >>> from_minutes("-4:00")
    -4.0
    """
    
    hh,mm = value.split(":")
    mm = float(mm)
    hh = float(hh)
    return (mm / 60) + hh

class QuerySet(QuerySet):
    
    def user(self, u):
        return self.filter(user=u,)
    
    ### by aircraft tags
    
    def turbine(self, f=True):
        kwarg={'plane__tags__icontains': 'TURBINE'}
        if not f:
            return self.exclude(**kwarg)
        return self.filter(**kwarg)
    
    def tailwheel(self, f=True):
        kwarg={'plane__tags__icontains': 'TAILWHEEL'}
        if not f:
            return self.exclude(**kwarg)
        return self.filter(**kwarg)
    
    def hp(self, f=True):
        q = Q(plane__tags__icontains='HP') |\
            Q(plane__tags__icontains='HIGH PERFORMANCE')
        if not f:
            return self.exclude(q)
        return self.filter(q)
    
    def complex_(self, f=True):
        kwarg={'plane__tags__icontains': 'COMPLEX'}
        if not f:
            return self.exclude(**kwarg)
        return self.filter(**kwarg)
    
    def jet(self, f=True):
        kwarg={'plane__tags__icontains': 'JET'}
        if not f:
            return self.exclude(**kwarg)
        return self.filter(**kwarg)
    
    ## by cat_class
    
    def cat_class(self, cat_class):
        return self.filter(plane__cat_class=cat_class)
    
    def pseudo_category(self, cat):
        """used for instrument currency"""
        if cat == "fixed_wing":
            return self.fixed_wing()
        elif cat == "glider":
            return self.glider()
        elif cat == "helicopter":
            return self.helicopter()
        
    def multi(self, f=True):
        kwarg={"plane__cat_class__in": (2,4)}
        if not f:
            return self.exclude(**kwarg)
        return self.filter(**kwarg)
    
    def single(self, f=True):
        kwarg={"plane__cat_class__in": (1,3)}
        if not f:
            return self.exclude(**kwarg)
        return self.filter(**kwarg)
    
    def sea(self, f=True):
        kwarg={"plane__cat_class__in": (3,4)}
        if not f:
            return self.exclude(**kwarg)
        return self.filter(**kwarg)
    
    def fixed_wing(self, f=True):
        kwarg={"plane__cat_class__lte": 4}
        if not f:
            return self.exclude(**kwarg)
        return self.filter(**kwarg)

    def sim(self, f=True):
        kwarg={"plane__cat_class__gte": 15}
        if not f:
            return self.exclude(**kwarg)
        return self.filter(**kwarg)
    
    def glider(self, f=True):
        kwarg={"plane__cat_class": 5}
        if not f:
            return self.exclude(**kwarg)
        return self.filter(**kwarg)
    
    def helicopter(self, f=True):
        kwarg={"plane__cat_class": 6}
        if not f:
            return self.exclude(**kwarg)
        return self.filter(**kwarg)
    
    ## by flight time
    
    def by_flight_time(self, col, f=True, eq=False, lt=None, gt=None):
        if lt:
            kwarg={col + "__lt": lt}
        elif gt:
            kwarg={col + "__gt": gt}
        elif eq:
            kwarg={col: eq}
        else:
            kwarg={col + "__gt": 0}
      
        if not f:
            return self.exclude(**kwarg)
        return self.filter(**kwarg)  
        
    ## convienience functions below
    
    def total(self, *args, **kwargs):
        return self.by_flight_time('total', *args, **kwargs)
    
    def pic(self, *args, **kwargs):
        return self.by_flight_time('pic', *args, **kwargs)
    
    def sic(self, *args, **kwargs):
        return self.by_flight_time('sic', *args, **kwargs)
    
    def solo(self, *args, **kwargs):
        return self.by_flight_time('solo', *args, **kwargs)
    
    def dual_g(self, *args, **kwargs):
        return self.by_flight_time('dual_g', *args, **kwargs)
    
    def dual_r(self, *args, **kwargs):
        return self.by_flight_time('dual_r', *args, **kwargs)
    
    def act_inst(self, *args, **kwargs):
        return self.by_flight_time('act_inst', *args, **kwargs)
    
    def sim_inst(self, *args, **kwargs):
        return self.by_flight_time('sim_inst', *args, **kwargs)
    
    def night(self, *args, **kwargs):
        return self.by_flight_time('night', *args, **kwargs)
    
    def xc(self, *args, **kwargs):
        return self.by_flight_time('xc', *args, **kwargs)
    
    def day_l(self, *args, **kwargs):
        return self.by_flight_time('day_l', *args, **kwargs)
    
    def night_l(self, *args, **kwargs):
        return self.by_flight_time('night_l', *args, **kwargs)
    
    def app(self, *args, **kwargs):
        return self.by_flight_time('app', *args, **kwargs)
    
    ####################################################
    
    def all_night(self, f=True, lt=None, gt=None):
        from django.db.models import F
        kwarg={"night": F('total')}
        if not f:
            return self.exclude(**kwarg)
        return self.filter(**kwarg)
    
    def all_pic(self, f=True, lt=None, gt=None):
        from django.db.models import F
        kwarg={"pic": F('total')}
        if not f:
            return self.exclude(**kwarg)
        return self.filter(**kwarg)
    
    def inst(self, f=True):
        q = Q(act_inst__gt=0) | Q(sim_inst__gt=0)
        if not f:
            return self.exclude(q)
        return self.filter(q)
    
    ## by route
    
    def p2p(self, f=True):
        kwarg={"route__p2p": True}
        if not f:
            return self.exclude(**kwarg)
        return self.filter(**kwarg)
    
    def only_p2p(self, f=True):
        kwarg={"route__p2p": True, "xc": 0}
        if not f:
            return self.exclude(**kwarg)
        return self.filter(**kwarg)
    
    #################@@##############
    
    def _db_agg(self, cn):
        """cn always equals a database column such as total or pic or xc
           returns the total for that field on the queryset after it has been
           properly filtered down"""
           
        if self == []:
            return 0
       
        return self.aggregate(Sum(cn)).values()[0] or 0
    
    def agg(self, cn):
        
        if cn in AGG_FIELDS:
            return self._db_agg(cn)
        
        elif cn in EXTRA_AGG:
            if cn == "day":
                night = self.sim(False)._db_agg('night')
                total = self.sim(False)._db_agg('total')
                return total - night
            
            if cn == "pic_night":
                return self.all_pic()._db_agg('night')
            
            try:
                if not cn.endswith("pic"):
                    return self.filter_by_column(cn)._db_agg('total')
                else:
                    return self.filter_by_column(cn)._db_agg('pic')
            except AttributeError:
                return 0.0      # return 0 if queryset is empty
            
        return "??"
    
    def filter_by_column(self, cn, *args, **kwargs):
        """filters the queryset to only include flights
           where the conditions exist"""
           
        if cn == "total_s" or cn == "total":
            return self.sim(False).total(*args, **kwargs)
            
        elif cn == "sim":
            return self.sim().total(*args, **kwargs)
            
        elif cn == 'complex':
            return self.complex_().total(*args, **kwargs)
            
        elif cn == 'hp':
            return self.hp().total(*args, **kwargs)
        
        elif cn == 'p2p':
            return self.p2p().total(*args, **kwargs)

        elif cn == 'turbine' or cn == 't_pic':
            return self.turbine().total(*args, **kwargs)
        
        elif cn == 'mt' or cn == 'mt_pic':
            return self.multi().turbine().pic(*args, **kwargs)
            
        elif cn == 'multi':
            return self.multi().total(*args, **kwargs)
        
        elif cn == 'm_pic':
            return self.multi().pic(*args, **kwargs)
        
        elif cn == 'sea' or cn == 'sea_pic':
            return self.sea().by_flight_time('pic', *args, **kwargs)
        
        elif cn == 'mes' or cn == 'mes_pic':
            return self.multi().sea().pic(*args, **kwargs)
        
        elif cn in DB_FIELDS:
            return getattr(self, cn)(*args, **kwargs)
       
    def custom_logbook_view(self, ff):
        assert ff.is_valid(), ff.errors
        
        self = ff.make_filter_kwargs(self)
        return self






