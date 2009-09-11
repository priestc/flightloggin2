from django.db.models import Q
from django.db.models.query import QuerySet

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
    
    def cplex(self, f=True):
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
        
    def multi(self, f=True):
        return self.filter()
        kwarg={"plane__cat_class__in": (2,4)}
        if not f:
            return self.exclude(**kwarg)
        return self.filter(**kwarg)
    
    def single(self, f=True):
        return self.filter()
        kwarg={"plane__cat_class__in": (1,3)}
        if not f:
            return self.exclude(**kwarg)
        return self.filter(**kwarg)
    
    def sea(self, f=True):
        return self.filter()
        kwarg={"plane__cat_class__in": (3,4)}
        if not f:
            return self.exclude(**kwarg)
        return self.filter(**kwarg)
    
    def fixed_wing(self, f=True):
        return self.filter()
        kwarg={"plane__cat_class__lte": 4}
        if not f:
            return self.exclude(**kwarg)
        return self.filter(**kwarg)
      
    def sim(self, f=True):
        return self.filter()
        kwarg={"plane__cat_class__gte": 15}
        if not f:
            return self.exclude(**kwarg)
        return self.filter(**kwarg)
    
    def glider(self, f=True):
        return self.filter()
        kwarg={"plane__cat_class": 5}
        if not f:
            return self.exclude(**kwarg)
        return self.filter(**kwarg)
    
    def helicopter(self, f=True):
        return self.filter()
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
