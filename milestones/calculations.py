import datetime

# checkmark and 'X' icons for use in showing if each milestone is met or not
V = '<span class="v">&#10003;</span>'
X = '<span class="x">&#10005;</span>'

def figure_dual60(qs):
    """
    Determine on what date your 60 days will expire
    (Used in all part 61 milestones) Also will get the total number of
    dual hours you've logged in the past 60 days
    """
    
    def get_date_of_5_hours(qs):
        """
        A seperate function so we can return out of the for loop
        """
        
        total_dual = 0
        for flight in qs:
            total_dual += flight.dual_r
            if total_dual > 5:
                return flight.date
    
    # calculate 60 days ago from today
    today = datetime.date.today()
    sixty_days_ago = today - datetime.timedelta(days=60)
    
    #filter flights between today and 60 days ago, count dual_r hours
    last_60_days = qs.filter(date__range=(sixty_days_ago, today)).agg('dual_r')
    
    # get the date of the 5th to last dual_r hour
    dual = qs.dual_r().order_by('-date')
    date = get_date_of_5_hours(dual)
    
    remain = 60 - (datetime.date.today() - date).days

    return {
                'dual_r':           last_60_days,
                'goal_dual_r':      5,
                'sixty_days_valid': remain > 0,
                'days':             remain,
                'overall':          V if remain > 0 else X,
           }

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

        # if the goal is a boolean, and my value matches, then use
        # values that will guarantee a pass in the next if block
        if isinstance(goal, bool) and bool(mine) == goal:
            mine = 2
            goal = 1
        else:
            mine = 0
            goal = 1

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


def p61_commercial(qs):
    """
    Determine Part 61.129 (commercial certificate) milestones
    """
    
    from django.utils.dateformat import format
    qs = qs.sim(False)
    
    from django.db.models import Count
    from route.models import Route
    
    #######
    
    # solo 3-point XC where max_width>50 and total dist is more than 150
    long_xc = Route.objects.filter(flight__in=qs.solo())\
                       .filter(max_width_land__gte=49)\
                       .filter(total_line_all__gte=150)\
                       .annotate(c=Count('routebase__land'))\
                       .filter(c__gt=3)\
                       .order_by('-flight__date')[:1]
   
    long_xc = ["%s - %s" % (format(x.flight.all()[0].date, "Y-m-d"),
                             x.simple_rendered) for x in long_xc]
    
    #######
    
    # long dual night XC more than 100 miles
    night_xc = Route.objects.filter(flight__in=qs.dual_r().night())\
                       .filter(total_line_land__gte=100)\
                       .order_by('-flight__date')[:1]
   
    night_xc = ["%s - %s" % (format(x.flight.all()[0].date, "Y-m-d"),
                             x.simple_rendered) for x in night_xc]
    
    #######
   
    inst = qs.dual_r().agg('sim_inst', float=True) +\
           qs.dual_r().agg('act_inst', float=True)
    
    ##################################################################
    
    # restrict all calculations to single engine planes
    #pic = qs.single()
    
    data = {
            'total':           (qs.agg('total'),                      250),
            't_powered':       (qs.powered().agg('total'),            100),
            't_airplane':      (qs.airplane().agg('pic'),              50),
            'pic':             (qs.agg('pic'),                        100),
            'pic_airplane':    (qs.airplane().agg('pic'),              50),
            'pic_xc':          (qs.p61_xc().agg('pic'),                50),
            'airplane_pic_xc': (qs.airplane().p61_xc().agg('pic'),     50),
            'inst_dual':       (qs.dual().agg('inst'),                 10),
            'complex':         (qs.complex().agg('total'),             10),
            }
                 
    return determine(data)


def part135ifr(qs):
    """ Part 135 IFR minimums """
    
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
    from django.utils.dateformat import format
    qs = qs.sim(False)
    
    from django.db.models import Count
    from route.models import Route
    
    #######
    
    # solo 3-point XC where max_width>50 and total dist is more than 150
    long_xc = Route.objects.filter(flight__in=qs.solo())\
                       .filter(max_width_land__gte=49)\
                       .filter(total_line_all__gte=150)\
                       .annotate(c=Count('routebase__land'))\
                       .filter(c__gt=3)\
                       .order_by('-flight__date')[:1]
   
    long_xc = ["%s - %s" % (format(x.flight.all()[0].date, "Y-m-d"),
                             x.simple_rendered) for x in long_xc]
    
    #######
    
    # long dual night XC more than 100 miles
    night_xc = Route.objects.filter(flight__in=qs.dual_r().night())\
                       .filter(total_line_land__gte=100)\
                       .order_by('-flight__date')[:1]
   
    night_xc = ["%s - %s" % (format(x.flight.all()[0].date, "Y-m-d"),
                             x.simple_rendered) for x in night_xc]
    
    #######
   
    inst = qs.dual_r().agg('sim_inst', float=True) +\
           qs.dual_r().agg('act_inst', float=True)
    
    ##################################################################
    
    data = {
                "total":    (qs.agg('total'),           40),
                "xc":       (qs.dual_r().agg('p61_xc'), 3),
                "dual_r":   (qs.agg('dual_r'),          20),
                "solo":     (qs.agg('solo'),            10),
                "night":    (qs.agg('night'),           3),
                "night_l":  (qs.agg('night_l'),         10),
                "solo_xc":  (qs.solo().agg('p61_xc'),   5),
                "inst":     (inst,                      3),
                "long_xc":  (long_xc,                   True),
                "night_xc": (night_xc,                  True),
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
