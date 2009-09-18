from django.db.models import Q
from django.db.models.query import QuerySet
from django.db.models import Sum

from constants import *

def to_minutes(flt):
    value = str(flt + 0.0)
    h,d = value.split(".")
    minutes = float("0." + d) * 60
    return str(h) + ":" + "%02.f" % minutes
    
def from_minutes(value):
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
        q = Q(plane__tags__icontains='HP') | Q(plane__tags__icontains='HIGH PERFORMANCE')
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
    
    def pic(self, f=True):
        kwarg={"pic__gt": 0}
        if not f:
            return self.exclude(**kwarg)
        return self.filter(**kwarg)
    
    def sic(self, f=True):
        kwarg={"sic__gt": 0}
        if not f:
            return self.exclude(**kwarg)
        return self.filter(**kwarg)
    
    def solo(self, f=True):
        kwarg={"solo__gt": 0}
        if not f:
            return self.exclude(**kwarg)
        return self.filter(**kwarg)
    
    def dual_g(self, f=True):
        kwarg={"dual_g__gt": 0}
        if not f:
            return self.exclude(**kwarg)
        return self.filter(**kwarg)
    
    def dual_r(self, f=True):
        kwarg={"dual_r__gt": 0}
        if not f:
            return self.exclude(**kwarg)
        return self.filter(**kwarg)
    
    def act_inst(self, f=True):
        kwarg={"act_inst__gt": 0}
        if not f:
            return self.exclude(**kwarg)
        return self.filter(**kwarg)
    
    def sim_inst(self, f=True):
        kwarg={"sim_inst__gt": 0}
        if not f:
            return self.exclude(**kwarg)
        return self.filter(**kwarg)
    
    def inst(self, f=True):
        q = Q(act_inst__gt=0) | Q(sim_inst__gt=0)
        if not f:
            return self.exclude(q)
        return self.filter(q)
    
    def night(self, f=True):
        kwarg={"night__gt": 0}
        if not f:
            return self.exclude(**kwarg)
        return self.filter(**kwarg)
    
    def all_night(self, f=True): ##FIXME
        kwarg={"night__gt": 0}
        if not f:
            return self.exclude(**kwarg)
        return self.filter(**kwarg)
    
    def xc(self, f=True):
        kwarg={"xc__gt": 0}
        if not f:
            return self.exclude(**kwarg)
        return self.filter(**kwarg)
    
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
    
    def day_l(self, f=True):
        kwarg={"day_l__gt": 0}
        if not f:
            return self.exclude(**kwarg)
        return self.filter(**kwarg)
    
    def night_l(self, f=True):
        kwarg={"night_l__gt": 0}
        if not f:
            return self.exclude(**kwarg)
        return self.filter(**kwarg)
    #night_l=property(night_l)
    
    def app(self, f=True):
        kwarg={"app__gt": 0}
        if not f:
            return self.exclude(**kwarg)
        return self.filter(**kwarg)
    #app=property(app)
    
    #################@@##############
    
    def _db_agg(self, cn):
        """cn always equals a database column such as total or pic or xc
           returns the total for that field on the queryset after it has been
           properly filtered down"""
       
        return self.aggregate(Sum(cn)).values()[0] or 0
    
    def agg(self, cn):
        
        if cn in AGG_FIELDS:
            return self._db_agg(cn)
        
        elif cn in EXTRA_AGG:
            if cn == "day":
                night = self._db_agg('night')
                total = self._db_agg('total')
                return total - night
            
            if not cn.endswith("pic"):
                return self.filter_by_column(cn)._db_agg('total')
            else:
                return self.filter_by_column(cn)._db_agg('pic')
        else:
            return "??"
    
    def filter_by_column(self, cn):
        """filters the queryset to only include flights
           where the conditions exist"""
           
        if cn == "total_s" or cn == "total":
            return self.sim(False)
            
        elif cn == "sim":
            return self.sim()
            
        elif cn == 'complex':
            return self.complex_()
            
        elif cn == 'hp':
            return self.hp()
        
        elif cn == 'p2p':
            return self.p2p()

        elif cn == 'turbine' or cn == 't_pic':
            return self.turbine()
        
        elif cn == 'mt' or cn == 'mt_pic':
            return self.multi().turbine()
            
        elif cn == 'multi':
            return self.multi()
        
        elif cn == 'm_pic':
            return self.multi().pic()
        
        elif cn == 'sea' or cn == 'sea_pic':
            return self.sea()
        
        elif cn == 'mes' or cn == 'mes_pic':
            return self.multi().sea()
        
        elif cn in DB_FIELDS:
            return getattr(self, cn)()
               






