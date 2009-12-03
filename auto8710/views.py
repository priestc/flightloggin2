from annoying.decorators import render_to
from django.db.models import Sum
from logbook.models import Flight

class FormLine(object):

    cats = None ## will be overwritten by subclasses
    
    total = "x&nbsp;"
    dual_r = "x&nbsp;"
    solo = "x&nbsp;"
    pic = "x&nbsp;"
    xc_dual_r = "x&nbsp;"
    xc_solo = "x&nbsp;"
    xc_pic = "x&nbsp;"
    inst = "x&nbsp;"
    night_dual_r = "x&nbsp;"
    night_l = "x&nbsp;"
    night_pic = "x&nbsp;"
    night_l_pic = "x&nbsp;"
    
    sic = "x&nbsp;"
    sic_xc = "x&nbsp;"
    sic_night = "x&nbsp;"
    sic_night_l = "x&nbsp;"
    
    def __init__(self, user):
        self.user = user        
        self.qs = Flight.objects.user(self.user)\
                 .filter(plane__cat_class__in=self.cats)\
                 
        self.determine()
 
    def determine(self):        
        main = self.qs.aggregate(
                    total=Sum('total'),
                    pic=Sum('pic'),
                    dual_r=Sum('dual_r'),
                    sic=Sum('sic'),
                    solo=Sum('solo'),
                    sim_inst=Sum('sim_inst'),
                    act_inst=Sum('act_inst'),
                    night_l=Sum('night_l'),
                 )
                 
        for field in ('total', 'pic', 'sic', 'dual_r',
                      'solo', 'night_l'):
            setattr(self, field, main[field] or "&nbsp;")
                                        
        self.inst = (main['act_inst'] or 0) + (main['sim_inst'] or 0)       
        if self.inst == 0:
            self.inst = "&nbsp;"
        
        ##########################################
            
        pic = self.qs.pic().aggregate(xc=Sum('xc'),
                                      night_l=Sum('night_l'),
                                      night=Sum('night'),
                                     )
                              
        self.xc_pic = pic['xc'] or "&nbsp;"
        self.night_pic = pic['night'] or "&nbsp;"
        self.night_l_pic = pic['night_l'] or "&nbsp;"
        
        ##########################################
        
        sic = self.qs.sic().aggregate(xc=Sum('xc'),
                                      night_l=Sum('night_l'),
                                      night=Sum('night'),
                                     )
                                             
        self.sic_xc = sic['xc'] or "&nbsp;"
        self.sic_night = sic['night'] or "&nbsp;"
        self.sic_night_l = sic['night_l'] or "&nbsp;"
        
        ##########################################
        
        dual_r = self.qs.dual_r().aggregate(xc=Sum('xc'),
                                            night=Sum('night'),
                                           )
                                           
        self.night_dual_r = dual_r['night'] or "&nbsp;"
        self.xc_dual_r = dual_r['xc'] or "&nbsp;"
        
        self.xc_solo = self.qs.solo().aggregate(xc=Sum('xc'))['xc'] or "&nbsp;"
        

class Airplane(FormLine):       
    cats = (1,2,3,4)
        
class Rotorcraft(FormLine):
    cats = (6,7)
    
class LTA(FormLine):
    cats = (12,13)
    
class Glider(FormLine):
    cats = (5, )
    
class PoweredLift(FormLine):
    cats = (14, )
    
class Sim(FormLine):
    cats = (15, 17)

class FTD(FormLine):
    cats = (16, 18)
    
class PCATD(FormLine):
    cats = (19, )

@render_to('8710.html')
def auto8710(request, shared, display_user):
    
    airplane = Airplane(display_user)
    rotorcraft = Rotorcraft(display_user)
    lta = LTA(display_user)
    glider = Glider(display_user)
    pl = PoweredLift(display_user)
    
    sim = Sim(display_user)
    ftd = FTD(display_user)
    pcatd = PCATD(display_user)
     
    return locals()
