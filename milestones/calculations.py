import datetime

from django.utils.datastructures import SortedDict
from django.utils.dateformat import format
from django.db.models import Count

from logbook.models import Flight
from logbook.constants import FIELD_TITLES
from route.models import Route
        
class Milestone(object):
    
    # checkmark and 'X' icons
    V = '<span class="v">&#10003;</span>'
    X = '<span class="x">&#10005;</span>'
    Q = '<span class="q">?</span>'

    def __init__(self, user):
        
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
        for value in data:
            
            mine = value['mine']
            title = value.get('display', None)
            goal = value['goal']
            
            title = (FIELD_TITLES.get(title, None) or
                     title or
                     "XXX")
            
            ## create a blank object so we can write
            ## arbitrary attributes to it.
            obj = {}
            
            obj['goal'] = goal
            obj['mine'] = mine
            obj['title'] = title
            obj['reg'] = value.get('reg', None)

            # if the goal is a boolean, and my value matches, then use
            # values that will guarantee a pass in the next if block
            if isinstance(goal, bool) and bool(mine) == goal:
                obj['icon'] = self.V
                obj['mine'] = " ".join(obj['mine'])
                obj['bool'] = True
                
            elif isinstance(goal, bool) and bool(mine) != goal:
                obj['icon'] = self.Q
                obj['mine'] = "<em>Not Found</em> *"
                obj['bool'] = True
                
            elif goal == "?":
                obj['icon'] = self.Q
                obj['mine'] = "<em>Unknown</em> **"
                obj['bool'] = True
                
            elif float(mine) >= float(goal):
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


    def figure_dual_60(self, cat_class=None):
        """
        Determine on what date your 60 days will expire
        (Used in all part 61 milestones) Also will get the total number of
        dual hours you've logged in the past 60 days
        cat_class must be an iterable
        """
        
        qs = self.all
        
        if cat_class:
            # filter by plane category/class if one is passed in
            qs = qs.filter(plane__cat_class__in=cat_class)
        
        def get_date_of_3_hours(qs):
            """
            A seperate function so we can return out of the for loop
            """
            
            total_dual = 0
            for flight in qs:
                total_dual += flight.dual_r
                if total_dual > 3:
                    return flight.date
        
        # calculate 60 days ago from today
        today = datetime.date.today()
        sda = today - datetime.timedelta(days=60)
        
        #filter flights between today and 60 days ago, count dual_r hours
        last_60_days = qs.filter(date__range=(sda, today)).agg('dual_r')
        
        
        
        # get the date of the 5th to last dual_r hour
        dual = qs.dual_r().order_by('-date')
        date = get_date_of_3_hours(dual)
        
        if not date:
            # logbook has no dual flights, return nothing
            return {}

        remain = 60 - (datetime.date.today() - date).days

        return {
                    'dual_r':    last_60_days,
                    'valid':     remain > 0,
                    'days':      abs(remain),
                    'overall':   self.V if remain > 0 else self.X,
               }

class Part61_Private(Milestone):
    
    top_title = "Part 61 Private Pilot Certificate"
    reg_letter = "a"
    
    def calculate(self):
        """
        Determine Part 61.109 (private pilot) milestones
        """
        
        self.dual_60 = self.figure_dual_60()
        
        # solo 3-point XC where max_width>50 and total dist is more than 150
        long_solo_xc = Route.objects.filter(flight__in=self.nosim.solo())\
                           .filter(max_width_land__gte=49)\
                           .filter(total_line_all__gte=150)\
                           .annotate(c=Count('routebase__land'))\
                           .filter(c__gt=3)\
                           .order_by('-flight__date')[:1]
       
        long_solo_xc = ["<b>%s</b> %s" % (format(x.flight.all()[0].date, "Y-M-d"),
                                 x.simple_rendered) for x in long_solo_xc]
        
        #######
        
        # long dual night XC more than 100 miles
        night_xc = Route.objects.filter(flight__in=self.nosim.dual_r().night())\
                           .filter(total_line_land__gte=100)\
                           .order_by('-flight__date')[:1]
       
        night_xc = ["<b>%s</b> %s" % (format(x.flight.all()[0].date, "Y-M-d"),
                                 x.simple_rendered) for x in night_xc] 
        
        ##################################################################
        
        qs = self.nosim
        
        data = [
                    dict(
                        mine=qs.agg('total'),
                        goal=40,
                        display='total',
                        reg="61.109(%s)" % self.reg_letter
                    ),

                    dict(
                        mine=qs.agg('dual_r'),
                        goal=20,
                        display="dual_r",
                        reg="61.109(%s)" % self.reg_letter
                    ),

                    dict(
                        mine=qs.dual_r().agg('p61_xc'),
                        goal=3,
                        display="Dual Part 61 XC",
                        reg="61.109(%s)(1)" % self.reg_letter
                    ),

                    dict(
                        mine=qs.agg('night'),
                        goal=3,
                        display="night",
                        reg="61.109(%s)(2)" % self.reg_letter
                    ),

                    dict(
                         mine=night_xc,
                         goal=True,
                         display="100NM Night XC",
                         reg="61.109(%s)(2)(i)" % self.reg_letter
                    ),                       

                    dict(
                        mine=qs.agg('night_l'),
                        goal=10,
                        display="night_l",
                        reg="61.109(%s)(2)(ii)" % self.reg_letter
                    ),

                    dict(
                        mine=qs.dual_r().agg('inst'),
                        goal=3,
                        display="Dual Instrument",
                        reg="61.109(%s)(3)" % self.reg_letter
                    ),

                    dict(
                        mine=self.dual_60.get('dual_r', 0),
                        goal=3,
                        display="Dual Last 60 days ***",
                        reg="61.109(%s)(4)" % self.reg_letter
                    ),

                    dict(
                        mine=qs.agg('solo'),
                        goal=10,
                        display="solo",
                        reg="61.109(%s)(5)" % self.reg_letter
                    ),

                    dict(
                        mine=qs.solo().agg('p61_xc'),
                        goal=5,
                        display="Solo Part 61 XC",
                        reg="61.109(%s)(5)(i)" % self.reg_letter
                    ),       
                        
                    dict(
                        mine=long_solo_xc,
                        goal=True,
                        display="Long Solo XC",
                        reg="61.109(%s)(5)(ii)" % self.reg_letter
                    ),

                    dict(
                        mine="?",
                        goal="?",
                        display="3 Fullstops at a Controlled Airfield",
                        reg="61.109(%s)(5)(iii)" % self.reg_letter
                    ),
                ]
        return data


class Part61_Commercial(Milestone):
    
    def relevent(self):
        """
        Determine if this milestone is relevent. Don't show this box if the
        user has more that 1500 hours and has passed all items
        """
        
        if self.overall_passed and self.all.agg('total', float=True) > 1500:
            return False
        
        return True
    
    def base_requirements(self):
        """
        Calculations for the commercial certificate that are consistent for
        all categories and classes
        """
        
        return [
                    dict(
                        mine=self.nosim.agg('total'),
                        goal=250,
                        display="Total as Pilot",
                        reg="61.129(%s)" % self.reg_letter,
                    )
                ]

class Part61_FixedWing_Commercial(Part61_Commercial):
        
    def calculate(self):
        """
        Determine Part 61.129(a/b) - fixed wing commercial
        certificate milestones
        """
        
        self.cat_class_qs = self.all.filter(plane__cat_class__in=self.cat_class)
        self.dual_60 = self.figure_dual_60(cat_class=self.cat_class)
        
        ######
        
        # solo 3-point XC where max_width>50 and total dist is more than 300
        long_solo_xc = Route.objects.filter(flight__in=self.all.solo())\
                           .filter(max_width_land__gte=249)\
                           .filter(total_line_all__gte=300)\
                           .annotate(c=Count('routebase__land'))\
                           .filter(c__gt=3)\
                           .order_by('-flight__date')[:1]
                           
        # format the display of this requirement
        long_solo_xc = ["<b>%s</b> - %s" % (format(x.flight.all()[0].date, "Y-m-d"),
                                 x.simple_rendered) for x in long_solo_xc]
        
        #######
        
        # long dual night XC more than 100 miles
        f = self.cat_class_qs.dual_r().total(gt=2).night()
        dual_night_xc = Route.objects.filter(flight__in=f)\
                           .filter(total_line_land__gte=100)\
                           .order_by('-flight__date')[:1]
       
        # format the display of this requirement
        dual_night_xc = ["<b>%s</b> - %s" % (format(x.flight.all()[0].date, "Y-m-d"),
                                 x.simple_rendered) for x in dual_night_xc]
        
        ##################################################################

        
        # get requirements from the parent classes
        data = self.base_requirements()
        
        data += [
                    dict(
                        mine=self.all.powered().agg('total'),
                        display="Total Powered Flight",
                        goal=100,
                        reg="61.129(%s)(1)" % self.reg_letter,
                    ),
                    
                    dict(
                        mine=self.all.fixed_wing().agg('pic'),
                        display="Total Fixed Wing",
                        goal=50,
                        reg="61.129(%s)(1)" % self.reg_letter,
                    ),
                    
                    dict(
                        mine=self.all.agg('pic'),
                        goal=100,
                        display="pic",
                        reg="61.129(%s)(2)" % self.reg_letter,
                    ),

                    dict(
                        mine=self.all.fixed_wing().agg('pic'),
                        display="PIC Airplane",
                        goal=50,
                        reg="61.129(%s)(2)(i)" % self.reg_letter,
                    ),

                    dict(
                        mine=self.all.p61_xc().agg('pic'),
                        display="PIC Part 61 XC",
                        goal=50,
                        reg="61.129(%s)(2)(ii)" % self.reg_letter,
                    ),

                    dict(
                        mine=self.all.fixed_wing().p61_xc().agg('pic'),
                        display="Fixed Wing PIC Part 61 XC",
                        goal=50,
                        reg="61.129(%s)(2)(ii)" % self.reg_letter,
                    ),

                    dict(
                        mine=self.all.dual_r().agg('inst'),
                        display="Instrument Dual",
                        goal=10,
                        reg="61.129(%s)(3)(i)" % self.reg_letter,
                    ),
                    
                    dict(
                        mine=self.cat_class_qs.dual_r().agg('inst'),
                        display="Instrument Dual %s" % self.cat_class_disp,
                        goal=5,
                        reg="61.129(%s)(3)(i)" % self.reg_letter,
                    ),

                    dict(
                        mine=self.all.dual_r().complex_().agg('total'),
                        display="Dual Complex",
                        goal=10,
                        reg="61.129(%s)(3)(ii)" % self.reg_letter,
                    ),
                    
                    dict(
                        mine=dual_night_xc,
                        display="Dual Long Night XC",
                        goal=True,
                        reg="61.129(%s)(3)(iv)" % self.reg_letter,
                    ),
                    
                    dict(
                        mine=self.dual_60.get('dual_r', 0),
                        display="%s Dual in the past 60 days" % self.cat_class_disp,
                        goal=3,
                        reg="61.129(%s)(3)(v)" % self.reg_letter,
                    ),
                    
                    dict(
                        mine=self.cat_class_qs.agg('solo'),
                        display="%s Solo" % self.cat_class_disp,
                        goal=10,
                        reg="61.129(%s)(4)" % self.reg_letter,
                    ),
                    
                    dict(
                        mine=long_solo_xc,
                        display="Long Solo XC",
                        goal=True,
                        reg="61.129(%s)(4)(i)" % self.reg_letter,
                    ),
                    
                    dict(
                        mine=self.all.solo().act_inst(False).agg('night'),
                        display="Solo VFR Night",
                        goal=5,
                        reg="61.129(%s)(4)(ii)" % self.reg_letter,
                    ),
                    
                    dict(
                        mine="?",
                        display="10 Landings at a Controlled Airfield",
                        goal="?",
                        reg="61.129(%s)(4)(ii)" % self.reg_letter,
                    ),
                ]
                
        return data

class Part61_SE_Commercial(Part61_FixedWing_Commercial):
        
    top_title = "Part 61 SE Initial Commercial Pilot Certificate"
    reg_letter = "a"
    cat_class_disp = "SE"
    cat_class = (1,3)

class Part61_ME_Commercial(Part61_FixedWing_Commercial):
        
    top_title = "Part 61 ME Initial Commercial Pilot Certificate"
    reg_letter = "b"
    cat_class_disp = "ME"
    cat_class = (2,4)
    
####################################################################
####################################################################

class Part135_IFR(Milestone):
    
    top_title = "Part 135 PIC"
    
    def calculate(self):
        """ Part 135 IFR minimums """
        
        # all instrument in a plane
        plane_inst = self.nosim.agg('inst', float=True)
        
        # all intrument in a simulator
        simulator_inst = self.onlysim.agg('sim_inst', float=True)
        
        # only use the first 25 hours of simulator instrument
        if simulator_inst > 25:
            simulator_inst = 25
        
        inst = str(float(simulator_inst) + float(plane_inst))
        
        ############

        data = [
        
                    dict(
                        mine=self.nosim.agg('total'),
                        goal=1200,
                        display='total',
                        reg="135.243(c)(2)",
                    ),
                             
                    dict(
                        mine=self.nosim.agg('night'),
                        goal=100,
                        display='night',
                        reg="135.243(c)(2)",
                    ),
                             
                    dict(
                        mine=self.nosim.agg('p2p'),
                        goal=500,
                        display='p2p',
                        reg="135.243(c)(2)",
                    ),
                             
                    dict(
                        mine=inst,
                        goal=75,
                        display="Instrument (50 in flight)",
                        reg="135.243(c)(2)",
                    ),
                    
                ]
        
        return data


class Part135_VFR(Milestone):
    
    top_title = "Part 135 PIC (VFR Only)"
    
    def calculate(self):
        """ Part 135 VFR minimums """
        
        qs = self.nosim
        
        data = [
                    dict(
                        mine=qs.agg('total'),
                        goal=500,
                        display='total',
                        reg="135.243(b)(2)",
                    ),
                                 
                    dict(
                        mine=qs.p2p().agg('night'),
                        goal=25,
                        display='night',
                        reg="135.243(b)(2)",
                    ),
                                 
                    dict(
                        mine=qs.agg('p2p'),
                        goal=100,
                        display='p2p',
                        reg="135.243(b)(2)",
                    ),
               ]                 
        
        return data

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
            extra_night = night_l - 20  #only the ones after 20

            if extra_night > 25:
                extra_night = 25  # limit extra night to 25
        
        night = self.nosim.agg('night', float=True)
        disp_night = "%.1f" % float(night+extra_night)
        
        ################################################# 

        data = [
        
                    dict(
                        mine=self.nosim.agg('total'),
                        goal=1500,
                        display='total',
                        reg="61.159(a)",
                    ),

                    dict(
                        mine=self.nosim.agg('atp_xc'),
                        goal=500,
                        display='atp_xc',
                        reg="61.159(a)(1)",
                    ),

                    dict(
                        mine=disp_night,
                        goal=100,
                        display='night',
                        reg="61.159(a)(2)",
                    ),
                        
                    dict(
                        mine=inst,
                        goal=75,
                        display="Instrument",
                        reg="61.159(a)(3)",
                    ),
                        
                    dict(
                        mine=self.nosim.agg('pic'),
                        goal=250,
                        display='pic',
                        reg="61.159(a)(4)",
                    ),
                        
                    dict(
                        mine=self.nosim.xc().agg('pic'),
                        goal=100,
                        display="PIC ATP Cross Country",
                        reg="61.159(a)(4)(i)",
                    ),
                        
                    dict(
                        mine=self.nosim.pic().agg('night'),
                        goal=25,
                        display="PIC Night",
                        reg="61.159(a)(4)(ii)",
                    ),
                
                ]
        
        return data
