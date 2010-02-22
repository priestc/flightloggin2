import datetime

from django.utils.datastructures import SortedDict
from django.utils.dateformat import format
from django.db.models import Count

from logbook.models import Flight
from logbook.constants import FIELD_TITLES
from route.models import Route
        
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
    
    if not date:
        return

    remain = 60 - (datetime.date.today() - date).days

    return SortedDict({
                'dual_r':           last_60_days,
                'goal_dual_r':      5,
                'sixty_days_valid': remain > 0,
                'days':             remain,
                'overall':          V if remain > 0 else X,
           })


class Milestone(object):
    
    # checkmark and 'X' icons
    V = '<span class="v">&#10003;</span>'
    X = '<span class="x">&#10005;</span>'

    def __init__(self, user):
        
        self.data = SortedDict()
        self.user = user
        self.all = Flight.objects.user(user)
        
        ## this is true if all items of the milestones are passed
        self.overall_passed = False
        
        self.nosim = self.all.sim(False)
        self.onlysim = self.all.sim(True)
        
        self.result = self.determine(self.calculate())
        
        try:
            self.relevent()
        except NotImplementedError:
            pass
        
    def relevent(self):
        raise NotImplementedError

    def determine(self, data):
        """
        Given a data dict, it goes through each item and creates a new dict
        based on if the minimums are met
        """
        
        result = []
        fails = 0
        for item,value in data.items():
            
            mine = value['mine']
            goal = value['goal']
            
            title = (value.get('display', None) or
                     FIELD_TITLES.get(item, None) or
                     "XXX")
            
            ## create a blank object so we can write
            ## arbitrary attributes to it.
            obj = {}
            
            obj['goal'] = goal
            obj['name'] = item
            obj['mine'] = mine
            obj['title'] = title
            obj['reg'] = value.get('reg', None)

            # if the goal is a boolean, and my value matches, then use
            # values that will guarantee a pass in the next if block
            if isinstance(goal, bool) and bool(mine) == goal:
                mine = 2
                goal = 1
                obj['bool'] = True
            elif isinstance(goal, bool) and bool(mine) != goal:
                mine = 0
                goal = 1
                obj['bool'] = True
                
            if float(mine) >= float(goal):
                # the requirement is met
                obj['icon'] = self.V
            else:
                # the requirement is not met
                obj['icon'] = self.X
                fails += 1
                
            result.append(obj)
                
        # if just one requirement is not met, overall good is false,
        # did not meet milestone
        if fails > 0:
            self.overall_passed = False
            self.overall_icon = self.X
        else:
            self.overall_passed = True
            self.overall_icon = self.V
                    
        return result


class Part61_Private(Milestone):
    
    top_title = "Part 61 Private Pilot Certificate"
    reg_letter = "a"
    
    def calculate(self):
        """
        Determine Part 61.109 (private pilot) milestones
        """
        
        # solo 3-point XC where max_width>50 and total dist is more than 150
        long_xc = Route.objects.filter(flight__in=self.nosim.solo())\
                           .filter(max_width_land__gte=49)\
                           .filter(total_line_all__gte=150)\
                           .annotate(c=Count('routebase__land'))\
                           .filter(c__gt=3)\
                           .order_by('-flight__date')[:1]
       
        long_xc = ["%s - %s" % (format(x.flight.all()[0].date, "Y-m-d"),
                                 x.simple_rendered) for x in long_xc]
        
        #######
        
        # long dual night XC more than 100 miles
        night_xc = Route.objects.filter(flight__in=self.nosim.dual_r().night())\
                           .filter(total_line_land__gte=100)\
                           .order_by('-flight__date')[:1]
       
        night_xc = ["%s - %s" % (format(x.flight.all()[0].date, "Y-m-d"),
                                 x.simple_rendered) for x in night_xc] 
        
        ##################################################################
        
        qs = self.nosim
        
        self.data["total"] =    dict(
                                    mine=qs.agg('total'),
                                    goal=40,
                                    reg="61.109(%s)" % self.reg_letter
                                )
                                
        self.data["dual_r"] =   dict(
                                    mine=qs.agg('dual_r'),
                                    goal=20,
                                    reg="61.109(%s)" % self.reg_letter
                                )
                                
        self.data["xc"] =       dict(
                                    mine=qs.dual_r().agg('p61_xc'),
                                    goal=3,
                                    display="Dual Part 61 XC",
                                    reg="61.109(%s)(1)" % self.reg_letter
                                )
                                
        self.data["night"] =    dict(
                                    mine=qs.agg('night'),
                                    goal=3,
                                    display="",
                                    reg="61.109(%s)(2)" % self.reg_letter
                                )
                                
        self.data["night_xc"] = dict(
                                     mine=night_xc,
                                     goal=True,
                                     display="100NM Night XC",
                                     reg="61.109(%s)(2)(i)" % self.reg_letter
                                )                        
                                
        self.data["night_l"] =  dict(
                                    mine=qs.agg('night_l'),
                                    goal=10,
                                    display="",
                                    reg="61.109(%s)(2)(ii)" % self.reg_letter
                                )
                                
        self.data["inst"] =     dict(
                                    mine=qs.dual_r().agg('inst'),
                                    goal=3,
                                    display="Dual Instrument",
                                    reg="61.109(%s)(3)" % self.reg_letter
                                )
                                
        self.data["solo"] =     dict(
                                    mine=qs.agg('solo'),
                                    goal=10,
                                    display="",
                                    reg="61.109(%s)(5)" % self.reg_letter
                                )
                                
        self.data["solo_xc"] =  dict(
                                    mine=qs.solo().agg('p61_xc'),
                                    goal=5,
                                    display="Solo Part 61 XC",
                                    reg="61.109(%s)(5)(i)" % self.reg_letter
                                )        
                                    
        self.data["long_xc"] =  dict(
                                    mine=long_xc,
                                    goal=True,
                                    display="Long Dual XC",
                                    reg="61.109(%s)(5)(ii)" % self.reg_letter
                                )
 
        return self.data


class Part61_Commercial(Milestone):
    
    top_title = "Part 61 Commercial Pilot Certificate"
    
    def relevent(self):
        """
        Determine if this milestone is relevent. Don't show this box if the
        user has more that 1500 hours and has passed all items
        """
        
        if self.overall_passed and self.all.agg('total', float=True) > 1500:
            return False
        
        return True
    
    def calculate(self):
        """
        Determine Part 61.129 (commercial certificate) milestones
        """
        
        qs = self.qs
        
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
       
        inst = self.nosim.dual_r().agg('sim_inst', float=True) +\
               self.nosim.dual_r().agg('act_inst', float=True)
        
        ##################################################################
        
        # restrict all calculations to single engine planes
        #pic = qs.single()
        
        data = SortedDict()
        
        self.data['total'] =          dict(
                                            mine=qs.agg('total'),
                                            goal=250,
                                      )
        
        self.data['t_powered'] =      dict(
                                            mine=qs.powered().agg('total'),
                                            goal=100,
                                      )
        
        self.data['t_airplane'] =     dict(
                                            mine=qs.fixed_wing().agg('pic'),
                                            goal=50,
                                      )
        
        self.data['pic'] =            dict(
                                            mine=qs.agg('pic'),
                                            goal=100,
                                      )
        
        self.data['pic_airplane'] =   dict(
                                            mine=qs.fixed_wing().agg('pic'),
                                            goal=50,
                                      )
        
        self.data['pic_xc'] =         dict(
                                            mine=qs.p61_xc().agg('pic'),
                                            goal=50,
                                      )
        
        self.data['airplane_pic_xc']= dict(
                                            mine=qs.fixed_wing().p61_xc().agg('pic'),
                                            goal=50,
                                      )
        
        self.data['inst_dual'] =      dict(
                                            mine=qs.dual_r().agg('inst'),
                                            goal=10,
                                      )
        
        self.data['complex'] =        dict(
                                            mine=qs.complex().agg('total'),
                                            goal=10,
                                      )
                     
        return self.data


####################################################################
####################################################################

class Part135_IFR(Milestone):
    
    top_title = "Part 135 PIC"
    
    def calculate(self):
        """ Part 135 IFR minimums """
        
        # all instrument in a plane
        plane_inst = self.nosim.agg('sim_inst', float=True) + \
                     self.nosim.agg('act_inst', float=True)
        
        # all intrument in a simulator
        simulator_inst = self.onlysim.agg('sim_inst', float=True)
        
        # only use the first 25 hours of simulator instrument
        if simulator_inst > 25:
            simulator_inst = 25
        
        inst = str(float(simulator_inst) + float(plane_inst))
        
        ############
        
        data = SortedDict()
        
        self.data['total'] = dict(
                                    mine=self.nosim.agg('total'),
                                    goal=1200,
                                    reg="135.243(c)(2)",
                             )
                             
        self.data['night'] = dict(
                                    mine=self.nosim.agg('night'),
                                    goal=100,
                                    reg="135.243(c)(2)",
                             )
                             
        self.data['p2p'] =   dict(
                                    mine=self.nosim.agg('p2p'),
                                    goal=500,
                                    reg="135.243(c)(2)",
                             )
                             
        self.data['inst'] =  dict(
                                    mine=inst,
                                    goal=75,
                                    display="Instrument (50 in flight)",
                                    reg="135.243(c)(2)",
                             )
        
        return self.data


class Part135_VFR(Milestone):
    
    top_title = "Part 135 PIC (VFR Only)"
    
    def calculate(self):
        """ Part 135 VFR minimums """
        
        qs = self.nosim
        
        self.data['total'] =     dict(
                                    mine=qs.agg('total'),
                                    goal=500,
                                    reg="135.243(b)(2)",
                                 )
                                 
        self.data['night_p2p'] = dict(
                                    mine=qs.p2p().agg('night'),
                                    goal=25,
                                    reg="135.243(b)(2)",
                                 )
                                 
        self.data['p2p'] =       dict(
                                    mine=qs.agg('p2p'),
                                    goal=100,
                                    reg="135.243(b)(2)",
                                )
                                    
        
        return self.data

#####################################################################
#####################################################################

class ATP(Milestone):
    
    top_title = "Part 61 Airplane ATP Certificate"
    
    def calculate(self):
        """ ATP minimums """
        
        # all real plane instrument
        plane_inst = self.nosim.agg('inst', float=True)
        
        # all simulator instrument             
        simulator_inst = self.onlysim.agg('sim_inst', float=True)
        
        # only the first 25 hours of simulator instrument can be used
        if simulator_inst > 25:
            simulator_inst = 25
        
        inst = simulator_inst + plane_inst
        
        ################
        
        # one hour for each night landings after 20, no more than 25 total
        extra_night=0
        night_l = self.nosim.agg('night_l', float=True)
        if night_l > 20:
            if night_l > 45:
                extra_night = 25
            else:
                extra_night = night_l
        
        night = self.nosim.agg('night', float=True)
        disp_night = "%.1f" % float(night+extra_night)
        
        ################################################# 
        
        data = SortedDict()
        
        self.data['total'] =     dict(
                                        mine=self.nosim.agg('total'),
                                        goal=1500,
                                        reg="61.159(a)",
                                 )
                                
        self.data['night'] =     dict(
                                        mine=disp_night,
                                        goal=100,
                                        reg="61.159(a)(2)",
                                 )
                                 
        self.data['atp_xc'] =    dict(
                                        mine=self.nosim.agg('atp_xc'),
                                        goal=500,
                                        reg="61.159(a)(1)",
                                 )
                                        
        self.data['inst'] =      dict(
                                        mine=inst,
                                        goal=75,
                                        display="Instrument",
                                        reg="61.159(a)(3)",
                                 )
                                        
        self.data['pic'] =       dict(
                                        mine=self.nosim.agg('pic'),
                                        goal=250,
                                        reg="61.159(a)(4)",
                                 )
                                        
        self.data['pic_xc'] =    dict(
                                        mine=self.nosim.xc().agg('pic'),
                                        goal=100,
                                        display="PIC ATP Cross Country",
                                        reg="61.159(a)(4)(i)",
                                 )
                                        
        self.data['pic_night'] = dict(
                                        mine=self.nosim.pic().agg('night'),
                                        goal=25,
                                        display="PIC Night",
                                        reg="61.159(a)(4)(ii)",
                                 )
        
        return self.data
