from annoying.decorators import render_to
from share.decorator import no_share

V = '<span class="v">&#10003;</span>'
X = '<span class="x">&#10005;</span>'

@no_share('other')
@render_to('milestones.html')
def milestones(request):
    from logbook.models import Flight
    qs = Flight.objects.user(request.display_user)
    
    part135 = part135ifr(qs)
    part135v = part135vfr(qs)
    atp = atp_calc(qs)
    
    return locals()

    
def smallbar(request, val, max_val):
    from small_progress_bar import SmallProgressBar
    return SmallProgressBar(float(val), float(max_val)).as_png()


def determine(data):
    """
    Given a data dict, it goes through each item and creates a new dict
    based on if the minimums are met
    """
    
    fails = 0
    result = {}
    for item,value in data.items():
        
        mine = value[0]
        goal = value[1]
               
        result[item] = mine
        result['goal_%s' % item] = goal

        if float(mine) >= float(goal):
            #the requirement is met
            result['icon_%s' % item] = V
        else:
            result['icon_%s' % item] = X
            fails += 1
            
    # if just one requirement is not met, overall good is false,
    # did not meet milestone
    if fails > 0:
        result['overall'] = X
    else:
        result['overall'] = V
    
    return result


def part135ifr(qs):
    """ Part 135 IFR minimums """
    
    ###########################################################################
    
    # only the first 25 hours of simulator instrument
    plane_inst = qs.sim(False).agg('sim_inst', float=True) + \
                 qs.sim(False).agg('act_inst', float=True)
                 
    simulator_inst = qs.sim(True).agg('sim_inst', float=True)
    
    if simulator_inst > 25:
        simulator_inst = 25
    
    inst = str(float(simulator_inst) + float(plane_inst))
    
    ############ part 135 IFR #################################################
    
    part135 = {}
    
    data = {
                'total': (qs.sim(False).agg('total'), 1200),
                'night': (qs.sim(False).agg('night'), 100),
                'p2p':   (qs.sim(False).agg('p2p'),   500),
                'inst':  (inst,                       75),
           }
    
    return determine(data)


def p61_private(qs):
    """
    Determine Part 61.109 (private pilot) milestones
    """
    
    qs = qs.sim(False)
    
    from django.db.models import Count
    # solo 3-point XC where max_width>50 and total dist is more than 150
    long_xc = qs.solo().filter(route__max_width_land__gte=49)\
                       .filter(route__total_line_all__gte=150)\
                       .annotate(c=Count('route__routebase__land'))\
                       .filter(c__gt=3)\
                       .values('date')[:5]
   
   
    ##################################################################
    
    data = {
                "total":    (qs.agg('total'),         40),
                "xc":       (qs.agg('p61_xc'),        3),
                "dual_r":   (qs.agg('dual_r'),        20),
                "solo":     (qs.agg('solo'),          10),
                "night":    (qs.agg('night'),         3),
                "night_l":  (qs.agg('night_l'),       10),
                "solo_xc":  (qs.solo().agg('p61_xc'), 5),
                "long_xc":  (long_xc,                 True),
            }
                 
    return determine(data)


def part135vfr(qs):
    """ Part 135 VFR minimums """
    
    qs = qs.sim(False)
    
    data = {
               'total':     (qs.agg('total'),       500),
               'night_p2p': (qs.p2p().agg('night'), 25),
               'p2p':       (qs.agg('p2p'),         100),
           }
    
    return determine(data)



def atp_calc(qs):
    """ ATP minimums """
    
    from logbook.models import Flight
    
    # all real plane instrument
    plane_inst = qs.sim(False).agg('sim_inst', float=True) +\
                 qs.sim(False).agg('act_inst', float=True)
    
    # all simulator instrument             
    simulator_inst = qs.sim(True).agg('sim_inst', float=True)
    
    # only the first 25 hours of simulator instrument can be used
    if simulator_inst > 25:
        simulator_inst = 25
    
    inst = simulator_inst + plane_inst
    
    
    # one hour for each night landings after 20, no more than 25 total
    extra_night=0
    night_l = qs.sim(False).agg('night_l', float=True)
    if night_l > 20:
        if night_l > 45:
            extra_night = 25
        else:
            extra_night = night_l
    
    night = qs.sim(False).agg('night', float=True)
    disp_night = "%.1f" % float(night+extra_night)
    
    ################################################# 
    
    data = {
                'total':     (qs.sim(False).agg('total'),       1500),
                'night':     (disp_night,                       100),
                'atp_xc':    (qs.sim(False).agg('atp_xc'),      500),
                'inst':      (inst,                             75),
                'pic':       (qs.sim(False).agg('pic'),         250),
                'pic_xc':    (qs.sim(False).xc().agg('pic'),    100),
                'pic_night': (qs.sim(False).pic().agg('night'), 25),
            }

    return determine(data)
