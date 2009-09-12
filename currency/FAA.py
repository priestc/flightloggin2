import re
from datetime import *
from dateutil.relativedelta import *

from django.db.models import Q

from plane.models import Plane
from logbook.models import Flight
from records.models import NonFlight

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
        return (start + relativedelta(months=+number + 1)).replace(day=1) + relativedelta(days=-1)
        
    else:
        raise ValueError("FL: Invalid unit formatting")
            
########################################
########################################

class FAA_Currency(object):
                           
    CURRENCY_DATA = {
                        "40":                  ("40y", "30d"),
                        
                        "flight_instructor":   ("24cm", "30d"),        # (name: duration, alert time) (24 calendar months, 30 days)
                        "landings":            ("90d", "10d"),
                        "flight_review":       ("24cm", "30d"),
                        
                        "first_over":          ("6cm", "30d"),
                        "second_over":         ("12cm", "30d"),
                        "third_over":          ("48cm", "30d"),
                        
                        "first_under":         ("12cm", "30d"),         # the time elapsed from the original exam date for each downgrade in calendar months
                        "second_under":        ("12cm", "30d"),
                        "third_under":         ("60cm", "30d")
                    }
                    
    medical_date = None
    medical_class = None        # this stuff is stored here so we don't have to hit the database multiple times
    over_40 = False
    pilot = False
    cfi = False
                    
    def __init__(self, user, today=None):
        self.user=user
        
        if not today:
            self.TODAY = date.today()
                    
    def _determine(self, method, start_date):
        """determine if the current date is before, after,
        or in the expire timeframe, or the alert timeframe."""
        
        expire_time   =   self.CURRENCY_DATA[method][0]     #get the alert and expire times based on the master dict
        alert_time    =   self.CURRENCY_DATA[method][1]
        
        expire_date = get_date(expire_time, start_date)
        alert_date = minus_alert(alert_time, expire_date)

        if self.TODAY > expire_date:                                 #today is later than expire date, EXPIRED
            return ("EXPIRED", expire_date)

        elif self.TODAY < expire_date and self.TODAY > alert_date:   #today is later than alert, but not past expired date, ALERT
            return ("ALERT", expire_date)

        elif self.TODAY < expire_date and self.TODAY < alert_date:   #today is before expire date, and before alert date, CURRENT
            return ("CURRENT", expire_date)
        
        else:
            assert False


    def landing(self, cat_class=0, tr=None, tail=False, night=False):
        """Returns the date of the third to last day or night landing,
        and whether or not it qualifies the user to be current"""
        
        if tr:
            if not night:
                last_three = Flight.objects.user(self.user).filter(plane__type=tr).\
                    filter(Q(day_l__gte=1) | Q(night_l__gte=1)).order_by('-date').values('date', 'day_l', 'night_l')[:3]
            
            if night:
                last_three = Flight.objects.user(self.user).\
                    filter(plane__type=tr, night_l__gte=1).order_by('-date').values('date', 'night_l')[:3]
            
        elif tail and cat_class > 0:  #cat_class above 0 is just a bug check
            plane = Plane.objects.filter(user=self.user, cat_class=cat_class, tags__icontains="TAILWHEEL")
            
            if not night:
                last_three = Flight.objects.user(self.user).\
                    filter(plane__in=plane).filter(Q(day_l__gte=1) | Q(night_l__gte=1)).order_by('-date').values('date', 'day_l', 'night_l')[:3]
                
            if night:
                last_three = Flight.objects.user(self.user).\
                    filter(plane__in=plane, night_l__gte=1).order_by('-date').values('date', 'night_l')[:3]
            
        elif cat_class < 15:  #forget simulators and FTD's (cat_classes above 15)
            if not night:
                last_three = Flight.objects.user(self.user).\
                    filter(plane__cat_class=cat_class).filter(Q(day_l__gte=1) | Q(night_l__gte=1)).order_by('-date').values('date', 'day_l', 'night_l')[:3]
                
            if night:
                last_three = Flight.objects.user(self.user).\
                    filter(plane__cat_class=cat_class, night_l__gte=1).order_by('-date').values('date', 'day_l', 'night_l')[:3]
        else:
            return
 
        total = 0
        for flight in last_three:
            total += flight['night_l']
            if not night:
                 total += flight['day_l']
            if total >= 3:
                start_date = flight['date']
                break;
                
        if total < 3:
            return ("NEVER", None, None)
            
        status, end_date = self._determine("landings", start_date)
        
        return (status, start_date, end_date)


    def flight_review(self):

        try:
            checkride_date = Flight.objects.filter(user=self.user, pilot_checkride=True).values_list("date", flat=True).reverse()[0]
            self.pilot = True
        except IndexError:
            checkride_date = None

        try:
            fr_date = Flight.objects.filter(user=self.user, flight_review=True).values_list("date", flat=True).reverse()[0]
            self.pilot = True
        except IndexError:
            fr_date = None

        ############

        if not fr_date and not checkride_date:
            return ("NEVER", None, None)

        elif checkride_date and not fr_date:
            start_date = checkride_date

        elif fr_date and not checkride_date:
            start_date = fr_date

        elif checkride_date > fr_date:
            start_date = checkride_date

        elif checkride_date < fr_date:
            start_date = fr_date

        ################################################################################

        status, end_date = self._determine("flight_review", start_date)

        return (status, start_date, end_date)


    def flight_instructor(self):
        try:
            checkride_date = Flight.objects.filter(user=self.user, cfi_checkride=True).values_list("date", flat=True).reverse()[0]
            self.cfi = True
        except IndexError:
            checkride_date = None

        try:
            refresher_date = NonFlight.objects.filter(user=self.user, non_flying=4).values_list("date", flat=True).reverse()[0]
            self.cfi = True
        except IndexError:
            refresher_date = None

        ############

        if not refresher_date and not checkride_date:           # no checkrides nor flight reviews in database, return "never"
            return ("NEVER", None, None)

        elif checkride_date and not refresher_date:
            start_date = checkride_date

        elif refresher_date and not checkride_date:
            start_date = refresher_date

        elif checkride_date > refresher_date:
            start_date = checkride_date

        elif checkride_date < refresher_date:
            start_date = refresher_date

        ############

        status, end_date = self._determine("flight_review", start_date)

        return (status, start_date, end_date)
        
    
    def _get_medical_info(self):
        """Finds out whether the user is over 40 based on their profile,
           also gets the last medical in their logbook by date and sets
           some variables based on when that medical was made, and what class it was"""
           
        try:
            dob = self.user.get_profile().dob            ## try to get the user's DOB from their profile, if no profile is made, assume they are over 40
        except AttributeError:
            dob = datetime.date(1915,7,21)
            
        status, end_date = self._determine("40", dob)
        self.over_40 = status == "EXPIRED"               ## if this comes back expired, user is over 40

        ###############
            
        try:
            last_medical = NonFlight.objects.filter(non_flying__in=[1,2,3]).order_by('-date')[0]        ## 1,2,3 = FAA medical exam codes
        except IndexError:
            return              #no medicals in logbook, return
            
        self.medical_date = last_medical.date
        self.medical_class = last_medical.non_flying


    def first_class(self):
    
        if not self.medical_date:
            self._get_medical_info()
            
        if not self.medical_class or not self.medical_class == 1:           #if medical was not issued as a first, it can never be a first
            return ("NEVER", None, None)
            
        if self.over_40:
            method = "first_over"
        else:
            method = "first_under"
            
            
        status, end_date = self._determine(method, self.medical_date)
        return (status, self.medical_date, end_date)


    def second_class(self):
    
        if not self.medical_date or not self.over_40:
            self._get_medical_info()

        if not self.medical_class or self.medical_class == 3:           #if medical was issued as a third, it can never be a second
            return ("NEVER", None, None)
            
        if self.over_40:
            method = "second_over"
        else:
            method = "second_under"

        status, end_date = self._determine(method, self.medical_date)
        return (status, self.medical_date, end_date)
    
    
    def third_class(self):
    
        if not self.medical_date or not self.over_40:
            self._get_medical_info()

        if not self.medical_class:
            return ("NEVER", None, None)
            
        if self.over_40:
            method = "third_over"
        else:
            method = "third_under"

        status, end_date = self._determine(method, self.medical_date)
        return (status, self.medical_date, end_date)     




