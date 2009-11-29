from annoying.decorators import render_to

V = '<span class="v">&#10003;</span>'
X = '<span class="x">&#10005;</span>'


@render_to('milestones.html')
def milestones(request, shared, display_user):
    from logbook.models import Flight
    qs = Flight.objects.user(display_user)
    
    part135 = part135ifr(qs)
    part135v = part135vfr(qs)
    atp = atp_calc(qs)
    
    return locals()
    
def smallbar(request, val, max_val):
    from small_progress_bar import SmallProgressBar
    return SmallProgressBar(float(val), float(max_val)).as_png()




    
def part135ifr(qs):
    
    ###########################################################################
    
    # only the first 25 hours of simulator instrument
    plane_inst = qs.sim(False).agg('sim_inst') + qs.sim(False).agg('act_inst')
    simulator_inst = qs.sim(True).agg('sim_inst')
    
    if simulator_inst > 25:
        simulator_inst = 25
    
    inst = simulator_inst + plane_inst
    
    ############ part 135 IFR #################################################
    
    part135 = {}
    
    my_numbers = {'total': "%.1f" % qs.sim(False).agg('total'),
                  'night': "%.1f" % qs.sim(False).agg('night'),
                  'p2p': "%.1f" % qs.sim(False).agg('p2p'),
                  'inst': inst}
                  
    goal_numbers = {'total': 1200,
                    'night': 100,
                    'p2p': 500,
                    'inst': 75}
    
    fails = 0
    for item in ('total', 'night', 'p2p', 'inst'):
        mine = my_numbers[item]
        goal = goal_numbers[item]
        
        part135[item] = mine
        part135['goal_%s' % item] = goal

        if float(mine) >= float(goal):
            #the requirement is met
            part135['icon_%s' % item] = V
        else:
            part135['icon_%s' % item] = X
            fails += 1
    
    # if just one requirement is not met, overall good is false,
    # did not meet milestone
    if fails > 0:
        part135['overall'] = X
    else:
        part135['overall'] = V

    return part135






def part135vfr(qs):
    
    ############ part 135 IFR #################################################
    
    part135 = {}
    
    my_numbers = {'total':     "%.1f" % qs.sim(False).agg('total'),
                  'night_p2p': "%.1f" % qs.sim(False).p2p().agg('night'),
                  'p2p':       "%.1f" % qs.sim(False).agg('p2p'),}
                  
    goal_numbers = {'total': 500,
                    'night_p2p': 25,
                    'p2p': 100}
    
    fails = 0
    for item in ('total', 'night_p2p', 'p2p'):
        mine = my_numbers[item]
        goal = goal_numbers[item]
        
        part135[item] = mine
        part135['goal_%s' % item] = goal

        if float(mine) >= float(goal):
            #the requirement is met
            part135['icon_%s' % item] = V
        else:
            part135['icon_%s' % item] = X
            fails += 1
    
    # if just one requirement is not met, overall good is false,
    # did not meet milestone
    if fails > 0:
        part135['overall'] = X
    else:
        part135['overall'] = V

    return part135




def atp_calc(qs):
    
    from logbook.models import Flight
    
    ###########################################################################
    
    # only the first 25 hours of simulator instrument
    plane_inst = qs.sim(False).agg('sim_inst') + qs.sim(False).agg('act_inst')
    simulator_inst = qs.sim(True).agg('sim_inst')
    
    if simulator_inst > 25:
        simulator_inst = 25
    
    inst = simulator_inst + plane_inst
    
    night_l = qs.sim(False).agg('night_l')
    if night_l > 20:
        if night_l > 45:
            extra_night = 25
        else:
            extra_night = night_l
    
    night = qs.sim(False).agg('night')
    
    ############ part 135 IFR #################################################
    
    atp = {}
    
    
    
    my_numbers = {'total':     "%.1f" % qs.sim(False).agg('total'),
                  'night':     "%.1f" % float(night+extra_night),
                  'atp_xc':    "%.1f" % qs.sim(False).agg('atp_xc'),
                  'inst':      inst,
                  'pic':       "%.1f" % qs.sim(False).agg('pic'),
                  'pic_xc':    "%.1f" % qs.sim(False).xc().agg('pic'),
                  'pic_night': "%.1f" % qs.sim(False).pic().agg('night'),}
                  
    goal_numbers = {'total': 1500,
                    'night': 100,
                    'atp_xc': 500,
                    'inst': 75,
                    'pic': 250,
                    'pic_xc': 100,
                    'pic_night': 25}
    
    fails = 0
    for item in ('total', 'night', 'atp_xc', 'inst', 'pic', 'pic_xc', 'pic_night'):
        mine = my_numbers[item]
        goal = goal_numbers[item]
        
        atp[item] = mine
        atp['goal_%s' % item] = goal

        if float(mine) >= float(goal):
            #the requirement is met
            atp['icon_%s' % item] = V
        else:
            atp['icon_%s' % item] = X
            fails += 1
    
    # if just one requirement is not met, overall good is false,
    # did not meet milestone
    if fails > 0:
        atp['overall'] = X
    else:
        atp['overall'] = V

    return atp
