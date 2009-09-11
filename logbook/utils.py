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
    #turbine=property(turbine)
    
    def tailwheel(self, f=True):
        kwarg={'plane__tags__icontains': 'TAILWHEEL'}
        if not f:
            return self.exclude(**kwarg)
        return self.filter(**kwarg)
    #tailwheel=property(tailwheel)
    
    def hp(self, f=True):
        q = Q(plane__tags__icontains='HP') | Q(plane__tags__icontains='HIGH PERFORMANCE')
        if not f:
            return self.exclude(q)
        return self.filter(q)
    #hp=property(hp)
    
    def complex(self, f=True):
        kwarg={'plane__tags__icontains': 'COMPLEX'}
        if not f:
            return self.exclude(**kwarg)
        return self.filter(**kwarg)
    #complex=property(complex)
    
    def jet(self, f=True):
        kwarg={'plane__tags__icontains': 'JET'}
        if not f:
            return self.exclude(**kwarg)
        return self.filter(**kwarg)
    #jet=property(jet)
    
    ## by cat_class
        
    def multi(self, f=True):
        kwarg={"plane__cat_class__in": (2,4)}
        if not f:
            return self.exclude(**kwarg)
        return self.filter(**kwarg)
    #multi=property(multi)
    
    def single(self, f=True):
        kwarg={"plane__cat_class__in": (1,3)}
        if not f:
            return self.exclude(**kwarg)
        return self.filter(**kwarg)
    #single=property(single)
    
    def sea(self, f=True):
        kwarg={"plane__cat_class__in": (3,4)}
        if not f:
            return self.exclude(**kwarg)
        return self.filter(**kwarg)
    #sea=property(sea)
    
    def fixed_wing(self, f=True):
        kwarg={"plane__cat_class__lte": 4}
        if not f:
            return self.exclude(**kwarg)
        return self.filter(**kwarg)
    #fixed_wing=property(fixed_wing)
      
    def sim(self, f=True):
        kwarg={"plane__cat_class__gte": 15}
        if not f:
            return self.exclude(**kwarg)
        return self.filter(**kwarg)
    #sim=property(sim)
    
    def glider(self, f=True):
        kwarg={"plane__cat_class": 5}
        if not f:
            return self.exclude(**kwarg)
        return self.filter(**kwarg)
    #glider=property(glider)
    
    def helicopter(self, f=True):
        kwarg={"plane__cat_class": 6}
        if not f:
            return self.exclude(**kwarg)
        return self.filter(**kwarg)
    #helicopter=property(helicopter)
    
    ## by flight time
    
    def pic(self, f=True):
        kwarg={"pic__gt": 0}
        if not f:
            return self.exclude(**kwarg)
        return self.filter(**kwarg)
    #pic=property(pic)
    
    def sic(self, f=True):
        kwarg={"sic__gt": 0}
        if not f:
            return self.exclude(**kwarg)
        return self.filter(**kwarg)
    #sic=property(sic)
    
    def solo(self, f=True):
        kwarg={"solo__gt": 0}
        if not f:
            return self.exclude(**kwarg)
        return self.filter(**kwarg)
    #sic=property(sic)
    
    def dual_g(self, f=True):
        kwarg={"dual_g__gt": 0}
        if not f:
            return self.exclude(**kwarg)
        return self.filter(**kwarg)
    #dual_g=property(dual_g)
    
    def dual_r(self, f=True):
        kwarg={"dual_r__gt": 0}
        if not f:
            return self.exclude(**kwarg)
        return self.filter(**kwarg)
    #dual_r=property(dual_r)
    
    def act_inst(self, f=True):
        kwarg={"act_inst__gt": 0}
        if not f:
            return self.exclude(**kwarg)
        return self.filter(**kwarg)
    #act_inst=property(act_inst)
    
    def sim_inst(self, f=True):
        kwarg={"sim_inst__gt": 0}
        if not f:
            return self.exclude(**kwarg)
        return self.filter(**kwarg)
    #sim_inst=property(sim_inst)
    
    def inst(self, f=True):
        q = Q(act_inst__gt=0) | Q(sim_inst__gt=0)
        if not f:
            return self.exclude(q)
        return self.filter(q)
    #inst=property(inst)
    
    def night(self, f=True):
        kwarg={"night__gt": 0}
        if not f:
            return self.exclude(**kwarg)
        return self.filter(**kwarg)
    #night=property(night)
    
    def all_night(self, f=True): ##FIXME
        kwarg={"night__gt": 0}
        if not f:
            return self.exclude(**kwarg)
        return self.filter(**kwarg)
    #night=property(night)
    
    def xc(self, f=True):
        kwarg={"xc__gt": 0}
        if not f:
            return self.exclude(**kwarg)
        return self.filter(**kwarg)
    #xc=property(xc)
    
    ## by route
    
    def p2p(self, f=True):
        kwarg={"route__p2p": True}
        if not f:
            return self.exclude(**kwarg)
        return self.filter(**kwarg)
    #night=property(night)
    
    def only_p2p(self, f=True):
        kwarg={"route__p2p": True, "xc": 0}
        if not f:
            return self.exclude(**kwarg)
        return self.filter(**kwarg)
    #only_p2p=property(only_p2p)
    
    def day_l(self, f=True):
        kwarg={"day_l__gt": 0}
        if not f:
            return self.exclude(**kwarg)
        return self.filter(**kwarg)
    #day_l=property(day_l)
    
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
        return self.aggregate(Sum(cn)).values()[0] or 0
    
    def agg(self, cn):
        
        if cn in AGG_FIELDS:
            return self._db_agg(cn)
        
        elif cn in EXTRA_AGG:
            if not '_' in cn:
                return self.filter_by_column(cn)._db_agg('total')
            
            time = cn.split("_")[-1]    ## pic, sic, total, etc
            if time in AGG_FIELDS:
                return self.filter_by_column(cn)._db_agg(time)
            else:
                return self.filter_by_column(cn)._db_agg('total')
        
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
            return self.complex()
            
        elif cn == 'hp':
            return self.hp()
        
        elif cn == 'p2p':
            return self.p2p()

        elif cn == 'turbine' or cn == 't_pic':
            return self.turbine()
        
        elif cn == 'mt' or cn == 'mt_pic':
            return self.multi().turbine()
            
        elif cn == 'multi' or cn == 'm_pic':
            return self.multi()
        
        elif cn == 'sea' or cn == 'sea_pic':
            return self.sea()
        
        elif cn == 'mes' or cn == 'mes_pic':
            return self.multi().sea()
        
        elif cn in DB_FIELDS:
            return getattr(self, cn)()
               




















    
