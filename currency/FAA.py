import re
from datetime import *
from dateutil.relativedelta import *

from django.db.models import Q

from plane.models import Plane
from logbook.models import Flight
from records.models import NonFlight

def latest(*args):
    """return the latest date"""
    dates = []
    for arg in args:
        if arg: dates.append(arg)
    
    if len(dates) == 1:     #if theres only one date, return it
        return dates[0]
    
    return max(*dates)      #there are more than one date, return the highest

def minus_alert(alert_time, expire):
    try:
        number, unit = re.match("^(\d+)([a-z]+)$", alert_time).groups()
    except:
        raise ValueError("FL: Invalid unit formatting")
    
    number = int(number)
        
    if unit == "d":
        return expire - timedelta(days=number)
    else:
        raise NotImplementedError("FL: Not yet")
        
#######################################

def get_date(expire_time, start):
    try:
        number, unit = re.match("^(\d+)([a-z]+)$", expire_time).groups()
    except:
        raise ValueError("FL: Invalid unit formatting")
    
    number = int(number)
        
    if unit == "d":
        return timedelta(days=number) + start
        
    elif unit == "m":
        return timedelta(months=number) + start

    elif unit == "y":
        return start + relativedelta(years=+number)

    elif unit == "cm":  #calendar months
        return (start + relativedelta(months=+number + 1))\
                    .replace(day=1) + relativedelta(days=-1)
        
    else:
        raise ValueError("FL: Invalid unit formatting")
            
########################################
########################################

class Currency(object):
    
    CURRENCY_DATA = {
                        "40":                  ("40y", "30d"),
                        
                        "flight_instructor":   ("24cm", "30d"),
                        "landings":            ("90d", "10d"),
                        "flight_review":       ("24cm", "30d"),
                        
                        "first_over":          ("6cm", "30d"),
                        "second_over":         ("12cm", "30d"),
                        "third_over":          ("24cm", "30d"),
                        
                        "instrument":          ("6cm", "30d"),
                        "ipc":                 ("6cm", "30d"),
             # time after instrument currency ends where an IPC is required
                        "need_ipc":            ("6cm", "30d"),
                        
            # the time elapsed from the original exam
            #date for each downgrade in calendar months
                        "first_under":         ("12cm", "30d"),
                        "second_under":        ("12cm", "30d"),
                        "third_under":         ("60cm", "30d")
                    }
    
    def __init__(self, user, today=None):
        self.user=user
        
        if not today:
            self.TODAY = date.today()
    
    def _determine(self, method, start_date, as_of_date=None):
        """determine if the current date is before, after,
        or in the expire timeframe, or the alert timeframe."""
        
        if not start_date:
            return ("NEVER", None)
        
        #get the alert and expire times based on the master dict
        expire_time   =   self.CURRENCY_DATA[method][0]
        alert_time    =   self.CURRENCY_DATA[method][1]
        
        expire_date = get_date(expire_time, start_date)
        alert_date = minus_alert(alert_time, expire_date)
        
        if not as_of_date:
            as_of_date = self.TODAY

        #today is later than expire date, EXPIRED
        if as_of_date > expire_date:
            return ("EXPIRED", expire_date)
        
        #today is later than alert, but not past expired date, ALERT
        elif as_of_date <= expire_date and as_of_date >= alert_date:
            return ("ALERT", expire_date)
        
        #today is before expire date, and before alert date, CURRENT
        elif as_of_date <= expire_date and as_of_date < alert_date:
            return ("CURRENT", expire_date)
        
        else:
            assert False, "Greater than / less than signs off"

class FAA_Landing(Currency):
    
    # (name: duration, alert time) (24 calendar months, 30 days)

    def landing(self, cat_class=0, tr=None, tail=False, night=False):
        """Returns the date of the third to last day or night landing,
        and whether or not it qualifies the user to be current"""
        
        if tr:                  # filter by type only
            if not night:
                last_three = Flight.objects.user(self.user)\
                    .filter(plane__type=tr)\
                    .filter(Q(day_l__gte=1) | Q(night_l__gte=1))\
                    .order_by('-date')\
                    .values('date', 'day_l', 'night_l')[:3]
            
            if night:
                last_three = Flight.objects.user(self.user)\
                    .filter(plane__type=tr, night_l__gte=1)\
                    .order_by('-date')\
                    .values('date', 'night_l')[:3]
            
        elif tail and cat_class > 0:  # filter by tailwheel and cat_class
            plane = Plane.objects.filter(user=self.user,
                                         cat_class=cat_class,
                                         tags__icontains="TAILWHEEL")
            
            if not night:
                last_three = Flight.objects.user(self.user)\
                    .filter(plane__in=plane)\
                    .filter(Q(day_l__gte=1) | Q(night_l__gte=1))\
                    .order_by('-date')\
                    .values('date', 'day_l', 'night_l')[:3]
                
            if night:
                last_three = Flight.objects.user(self.user)\
                    .filter(plane__in=plane, night_l__gte=1)\
                    .order_by('-date')\
                    .values('date', 'night_l')[:3]
            
        elif cat_class < 15:  #filter by just cat_class
            if not night:
                last_three = Flight.objects.user(self.user)\
                    .filter(plane__cat_class=cat_class)\
                    .filter(Q(day_l__gte=1) | Q(night_l__gte=1))\
                    .order_by('-date')\
                    .values('date', 'day_l', 'night_l')[:3]
                
            if night:
                last_three = Flight.objects.user(self.user)\
                    .filter(plane__cat_class=cat_class)\
                    .filter(night_l__gte=1)\
                    .order_by('-date')\
                    .values('date', 'night_l')[:3]
        else:
            return "ERROR"
 
        total = 0
        for flight in last_three:
            total += flight.get('night_l',0) + flight.get('day_l',0)
            if total >= 3:
                start_date = flight['date']
                break;
                
        if total < 3:
            return ("NEVER", None, None)
            
        status, end_date = self._determine("landings", start_date)
        
        return (status, start_date, end_date)

class FAA_Certs(Currency):

    has_bfr_event = False
    has_cfi_event = False

    def flight_review(self):

        try: # get latest checkride or flight review
            flight_date = Flight.objects\
                .user(self.user)\
                .filter(Q(pilot_checkride=True) | Q(flight_review=True))\
                .values_list("date", flat=True)\
                .latest()
                
            self.has_bfr_event = True
            
        except Flight.DoesNotExist:
            flight_date = None
            
        try: ## try to get wings program
            event_date = NonFlight.objects\
                                  .filter(user=self.user, non_flying=6)\
                                  .values_list("date", flat=True)\
                                  .latest()
                                      
            self.pilot_event = True
        except NonFlight.DoesNotExist:
            event_date = None

        ############

        if not event_date and not flight_date:
            return ("NEVER", None, None)
        
        start_date = latest(event_date, flight_date)
        
        status, end_date = self._determine("flight_review", start_date)
        return (status, start_date, end_date)

    ###########################################################################
    
    def flight_instructor(self):
        try:
            checkride_date = Flight.objects\
                    .filter(user=self.user, cfi_checkride=True)\
                    .values_list("date", flat=True)\
                    .latest()
                    
            self.has_cfi_event = True
            
        except Flight.DoesNotExist:
            checkride_date = None
        
        #############################
        
        try:
            refresher_date = NonFlight.objects\
                    .filter(user=self.user, non_flying=4)\
                    .values_list("date", flat=True)\
                    .latest()
                    
            self.cfi = True
        except NonFlight.DoesNotExist:
            refresher_date = None

        ############

        if not refresher_date and not checkride_date:
            # no checkrides nor flight reviews in database, return "never"
            return ("NEVER", None, None)

        start_date = latest(refresher_date, checkride_date)
        status, end_date = self._determine("flight_review", start_date)
        return (status, start_date, end_date)
    
    ###########################################################################

class FAA_Instrument(Currency):
    
    fake_class = "fixed_wing"
    
    def ipc(self):
        """
        Determine of the last IPC is still valid
        """
        
        try:
            ipc_date = Flight.objects.user(self.user)\
                                 .filter(ipc=True)\
                                 .values_list("date", flat=True)\
                                 .latest()    
                                        
        except Flight.DoesNotExist:
            ipc_date = None
        
        if not ipc_date:       # no ipc's in database, return "never"
            return ("NEVER", None, None)
        
        status, end_date = self._determine("ipc", ipc_date)
        return (status, ipc_date, end_date)
        
    def six(self):
        """
        Get the dates of the last 6 appoaches
        """
        
        last_six = Flight.objects\
                    .user(self.user)\
                    .pseudo_category(self.fake_class)\
                    .app()\
                    .order_by('-date')\
                    .values('date', 'app')[:6]
        
        app_date = None
        total = 0
        for flight in last_six:
            total += flight['app']
            if total >= 6:
                app_date = flight['date']
                break;
            
        status, end = self._determine("instrument", app_date)
        return status, app_date, end
    
    def ht(self, ht):
        """
        Get the dates of the last 'holding' or 'tracking'
        """
        kwarg = {ht: True}
        
        try:
            ht_date = Flight.objects\
                     .user(self.user)\
                     .pseudo_category(self.fake_class)\
                     .filter(**kwarg)\
                     .values_list('date', flat=True)\
                     .latest()
        
        except Flight.DoesNotExist:
            ht_date = None
        
        status, end = self._determine("instrument", ht_date)
        return status, ht_date, end
        
    def determine_overall_status(self):
        self.ipc_status, self.ipc_start, self.ipc_end = self.ipc()
        self.six_status, self.six_start, self.six_end = self.six()
        self.h_status, self.h_start, self.h_end = self.ht('holding')
        self.t_status, self.t_start, self.t_end = self.ht('tracking')
        
        alert = False; expired = False
        for item in ("six", "h", "t"):
            st = getattr(self, "%s_status" % item)
            if st == "ALERT":
                alert = True
            if st == 'EXPIRED' or st == 'NEVER':
                expired = True
               
        if alert and not expired:
            #if any are alert and none are expired
            self.overall_status = "ALERT"
            
        elif not expired:
            # if any none are expired
            self.overall_status = "CURRENT"
        else:
            # if at least one is expired
            self.overall_status = "EXPIRED"
            
        #ipc trumps all    
        if self.ipc_status == "CURRENT":
            self.overall_status = "CURRENT"
            
        if self.ipc_status == "ALERT" and expired:
            self.overall_status = "ALERT"
            
        if self.ipc_status == "ALERT" and not expired:
            self.overall_status = "CURRENT"
            
        return self.overall_status
    
        
class FAA_Medical(Currency):
    
    medical_date = None
    medical_class = None
    
    def _get_medical_info(self):
        """Finds out whether the user is over 40 based on their profile,
           also gets the last medical in their logbook by date and sets
           some variables based on when that medical was made, and what
           class it was
        """
        
        try:
            last_medical = NonFlight.objects\
                            .filter(user=self.user, non_flying__in=[1,2,3])\
                            .latest()
                         
        except NonFlight.DoesNotExist:
            return None             #no medicals in logbook
        
        from profile.models import Profile
        try:
            ## try to get the user's DOB from their profile, if no profile
            # is made, assume they are over 40
            dob = Profile.get_for_user(self.user).dob
        except AttributeError, Profile.DoesNotExist:
            dob = datetime.date(1915,7,21)
            
        status, end_date = self._determine("40", dob, as_of_date=last_medical.date)
        
        ## if this comes back expired, user is over 40
        self.over_40 = (status == "EXPIRED")
        
        ###############
            
        self.medical_date = last_medical.date
        self.medical_class = last_medical.non_flying


    def first_class(self):
    
        if not self.medical_date:
            self._get_medical_info()
        
        #if medical was not issued as a first, it can never be a first    
        if not self.medical_class or not self.medical_class == 1:
            return ("NEVER", None, None)
            
        if self.over_40:
            method = "first_over"
        else:
            method = "first_under"
            
            
        status, end_date = self._determine(method, self.medical_date)
        return (status, self.medical_date, end_date)


    def second_class(self):
    
        if not self.medical_date:
            self._get_medical_info()

        #if medical was issued as a third, it can never be a second
        if not self.medical_class or self.medical_class == 3:
            return ("NEVER", None, None)
            
        if self.over_40:
            method = "second_over"
        else:
            method = "second_under"

        status, end_date = self._determine(method, self.medical_date)
        return (status, self.medical_date, end_date)
    
    
    def third_class(self):
    
        if not self.medical_date:
            self._get_medical_info()

        if not self.medical_class:
            return ("NEVER", None, None)
            
        if self.over_40:
            method = "third_over"
        else:
            method = "third_under"

        status, end_date = self._determine(method, self.medical_date)
        return (status, self.medical_date, end_date)     




