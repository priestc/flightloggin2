from django.db.models import Q
from django.db.models.query import QuerySet
from django.db.models import Sum
from constants import AGG_FIELDS, EXTRA_AGG, DB_FIELDS
from main.mixins import UserMixin

class FlightQuerySet(QuerySet, UserMixin):
        
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
            return self.curr_fixed_wing()
        elif cat == "glider":
            return self.glider()
        elif cat == "helicopter":
            return self.curr_helicopter()
        
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
    
    def curr_fixed_wing(self, f=True):
        """ fixed wing plus airplane sim and airplane FTD
            for instrument currency
        """
        
        kwarg={"plane__cat_class__in": (1,2,3,4,16,15)}
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
    
    def curr_helicopter(self, f=True):
        """ filter helicopter, heli ftd and heli sim"""
        
        kwarg={"plane__cat_class__in": (6,17,18)}
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
    
    def by_route_val(self, col, f=True, eq=False, lt=None, gt=None):
        if lt:
            kwarg={"route__%s__lt" % col: lt}
        elif gt:
            kwarg={"route__%s__gt" % col: gt}
        elif eq:
            kwarg={"route__%s" % col: eq}
        else:
            kwarg={"route__%s__gt" % col: 0}
      
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
    
    def atp_xc(self, f=True):
        kwarg={"route__max_width_all__gt": 49}
        if not f:
            return self.exclude(**kwarg)
        return self.filter(**kwarg)
    
    def line_dist(self, f=True):
        kwarg={"route__total_line_all__gt": 0}
        if not f:
            return self.exclude(**kwarg)
        return self.filter(**kwarg)
        
    #################@@##############
    
    def _db_agg(self, cn):
        """cn always equals a database column such as total or pic or xc.
           returns the total for that field on the queryset after it has been
           properly filtered down"""
           
        if self == []:
            return 0
        
        if cn == 'line_dist':
            return self.aggregate(Sum('route__total_line_all')).values()[0] or 0
       
        return self.aggregate(Sum(cn)).values()[0] or 0
    
    def agg(self, cn, format='decimal', float=False):
        """
        Aggregate this queryset based on the field passed. Always returns a string
        """
        
        ret = None
        
        if cn in AGG_FIELDS:
            ret = self._db_agg(cn)
        
        elif cn in EXTRA_AGG:
            if cn == "day":
                #day is special, so it gets done here instead of 'filter_by_column'
                night = self.sim(False)._db_agg('night')
                total = self.sim(False)._db_agg('total')
                ret = total - night
            
            if cn == "pic_night":
                ret = self.all_pic()._db_agg('night')
            
            if cn == "line_dist":
                ret = self._db_agg('line_dist')

            if not cn.endswith("pic") and not ret:
                ret = self.filter_by_column(cn)._db_agg('total')
            elif not ret:
                ret = self.filter_by_column(cn)._db_agg('pic')
            
        from logbook.utils import proper_format
        if not float:
            return proper_format(ret, cn, format)
        else:
            return ret
    
    def filter_by_column(self, cn, *args, **kwargs):
        """filters the queryset to only include flights
           where the conditions exist"""
           
        if cn == "total_s" or cn == "total":
            return self.sim(False).total(*args, **kwargs)
        
        if cn == 'day':
            return self.sim(False).total(*args, **kwargs) - \
                     self.sim(False).night(*args, **kwargs)
            
        elif cn == "sim":
            return self.sim().total(*args, **kwargs)
            
        elif cn == 'complex':
            return self.complex_().total(*args, **kwargs)
            
        elif cn == 'hp':
            return self.hp().total(*args, **kwargs)
        
        elif cn == 'p2p':
            return self.p2p().total(*args, **kwargs)

        elif cn == 'turbine':
            return self.turbine().total(*args, **kwargs)
        
        elif cn == 't_pic':
            return self.turbine().pic(*args, **kwargs)
        
        elif cn == 'mt':
            return self.multi().turbine().total(*args, **kwargs)
            
        elif cn == 'mt_pic':
            return self.multi().turbine().pic(*args, **kwargs)
            
        elif cn == 'multi':
            return self.multi().total(*args, **kwargs)
        
        elif cn == 'single':
            return self.single().total(*args, **kwargs)
        
        elif cn == 'single_pic':
            return self.single().pic(*args, **kwargs)
        
        elif cn == 'm_pic':
            return self.multi().pic(*args, **kwargs)
        
        elif cn == 'sea':
            return self.sea().total(*args, **kwargs)
            
        elif cn == 'sea_pic':
            return self.sea().pic(*args, **kwargs)
        
        elif cn == 'mes':
            return self.multi().sea().total(*args, **kwargs)
        
        elif cn == 'jet':
            return self.jet().total(*args, **kwargs)
        
        elif cn == 'tail':
            return self.tailwheel().total(*args, **kwargs)
        
        elif cn == 'jet_pic':
            return self.jet().pic(*args, **kwargs)
        
        elif cn == 'mes_pic':
            return self.multi().sea().pic(*args, **kwargs)
        
        elif cn == 'atp_xc':
            return self.sim(False).atp_xc().total(*args, **kwargs)
        
        elif cn == 'line_dist':
            return self.sim(False).by_route_val('total_line_all', *args, **kwargs)
        
        elif cn == 'max_width':
            return self.sim(False).by_route_val('max_width_all', *args, **kwargs)
        
        elif cn in DB_FIELDS:
            return getattr(self, cn)(*args, **kwargs)
       
    def custom_logbook_view(self, ff):
        assert ff.is_valid(), ff.errors
        
        self = ff.make_filter_kwargs(self)
        return self

    def add_column(self, *args):
        for arg in args:
            if arg == 'day':
                self = self.extra(select={'day': "total - night"})
            
            elif arg == 'instrument':
                self = self.extra(select={'instrument': "act_inst + sim_inst"})
            
            elif arg == 'distance':
                self = self.extra(select={"distance":'route_route.total_line_all'})
            
            elif arg == 'speed':
                self = self.extra(select={"speed":
                    """route_route.total_line_all / total"""})
                       
            elif arg == 'multi':
                self = self.extra(select={'multi':
                    """CASE WHEN plane_plane.cat_class in (2,4)
                       THEN total
                       ELSE 0
                       END
                    """
                })
                
            elif arg == 'm_pic':
                self = self.extra(select={'m_pic':
                    """CASE WHEN plane_plane.cat_class in (2,4)
                       THEN pic
                       ELSE 0
                       END
                    """
                })
                
            elif arg == 'single':
                self = self.extra(select={'single':
                    """CASE WHEN plane_plane.cat_class in (1,3)
                       THEN total
                       ELSE 0
                       END
                    """
                })
                
            elif arg == 'single_pic':
                self = self.extra(select={'single':
                    """CASE WHEN plane_plane.cat_class in (1,3)
                       THEN pic
                       ELSE 0
                       END
                    """
                })
            
            elif arg == 'sea':
                self = self.extra(select={'sea':
                    """CASE WHEN plane_plane.cat_class in (3,4)
                       THEN total
                       ELSE 0
                       END
                    """
                })
                
            elif arg == 'sea_pic':
                self = self.extra(select={'sea_pic':
                    """CASE WHEN plane_plane.cat_class in (3,4)
                       THEN pic
                       ELSE 0
                       END
                    """
                })
                
            elif arg == 'p2p':
                self = self.extra(select={'p2p':
                    """CASE WHEN route_route.p2p
                       THEN total
                       ELSE 0
                       END
                    """
                })
            
        return self
