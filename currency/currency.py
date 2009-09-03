import re
from datetime import *
from dateutil.relativedelta import *

from django.db.models import Q

from logbook.models import Flight
from records.models import NonFlight

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
        return timedelta(years=number) + start

    elif unit == "cm":
        return (start + relativedelta(months=+number + 1)).replace(day=1) + relativedelta(days=-1)
        
    else:
        raise ValueError("FL: Invalid unit formatting")
            
########################################
########################################

class FAA_Currency(object):
                           
    CURRENCY_DATA = {
                        "flight_instructor":   ("24cm", "30d"),        # (name, duration, alert time)
                        "landings":            ("90d", "10d"),
                        "flight_review":       ("24cm", "30d"),
                        "medical_over":        ("6cm", "12cm", "48cm"),
                        "medical_under":       ("12cm", "12cm", "60cm"),         # the time elapsed from the original exam date for each downgrade in calendar months
                    }
                    
    def __init__(self, user):
        self.user=user
                    
    def _determine(self, method, start_date):
        """determine if the current date is before, after, or in the alert timeframe."""
        
        TODAY = date.today()

        expire_time   =   self.CURRENCY_DATA[method][0]     #get the alert and expire times based on the master dict
        alert_time    =   self.CURRENCY_DATA[method][1]
        
        expire_date = get_date(expire_time, start_date)
        alert_date = get_date(expire_time, start_date)

        if TODAY > expire_date:                                 #today is later than expire date, EXPIRED
            return ("EXPIRED", expire_date)

        elif TODAY < expire_date and TODAY > alert_date:       #today is later than alert, but not past expired date, ALERT
            return ("ALERT", expire_date)

        elif TODAY < expire_date and TODAY < alert_date:       #today is before expire date, and before alert date, CURRENT
            return ("CURRENT", expire_date)
        
        else:
            assert False


    def day_landing(self, cat_class=0, tr=None, tail=False):
        """Returns the date of the third to last day/night landing,
        and whether or not it qualifies the user to be current"""
        
        last_three = Flight.objects.filter(user=self.user, plane__cat_class=cat_class).filter(Q(day_l__gte=1) | Q(night_l__gte=1)).order_by('-date').values('date', 'day_l', 'night_l')[:3]
        
        total = 0
        for flight in last_three:
            total += flight['night_l'] + flight['day_l']
            if total >= 3:
                start_date = flight['date']
                break;
                
        if total < 3:
            return ("NEVER", None, None)
            
        status, end_date = self._determine("landings", start_date)
        
        return (status, start_date, end_date)
        
        


    def night_landing(self, cat_class=0, tr=None, tail=False):
        """Returns the date of the third to last night landing,
        and whether or not it qualifies the user to be current"""
        
        last_three = Flight.objects.filter(user=self.user, night_l__gte=1, plane__cat_class=cat_class).order_by('-date').values('date', 'night_l')[:3]

        total = 0
        for flight in last_three:
            total += flight['night_l']
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
        except IndexError:
            checkride_date = None

        try:
            fr_date = Flight.objects.filter(user=self.user, flight_review=True).values_list("date", flat=True).reverse()[0]
        except IndexError:
            fr_date = None

        ############

        if not fr_date and not checkride_date:
            return "NEVER"

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
        except IndexError:
            checkride_date = None

        try:
            refresher_date = NonFlight.objects.filter(user=self.user, non_flying=4).values_list("date", flat=True).reverse()[0]
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








