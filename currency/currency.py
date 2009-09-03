import re
from datetime import *
from dateutil.relativedelta import *

from logbook.models import Flight
from records.models import NonFlight

def translate_units(value):
    try:
        number, unit = re.match("^(\d+)([a-z]+)$", value).groups()
    except:
        raise ValueError("FL: Invalid unit formatting")
    
    number = int(number)
        
    if unit == "d":
        return timedelta(days=number)
        
    elif unit == "m":
        return timedelta(months=number)

    elif unit == "y":
        return timedelta(years=e_number)

    elif unit == "cm":
        return relativedelta(months=+number + 1).replace(day=1) + relativedelta(days=-1)
        
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
                    
    def determine(self, method, start_date):
        """determine if the current date is before, after, or in the alert timeframe."""
        
        TODAY = date.today()

        expire_time   =   self.CURRENCY_DATA[method][0]     #get the alert and expire times based on the master dict
        alert_time    =   self.CURRENCY_DATA[method][1]
        
        expire_date = translate_units(expire_time) + start_date
        alert_date = translate_units(expire_time) + start_date
        

        if TODAY > expire_date:                                 #today is later than expire date, EXPIRED
            return "EXPIRED"

        elif TODAY < expire_date and TODAY > alert_delta:       #today is later than alert, but not past expired date, ALERT
            return "ALERT"

        elif TODAY < expire_date and TODAY < alert_delta:       #today is before expire date, and before alert date, CURRENT
            return "CURRENT"
        
        else:
            assert False

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

        return self.determine("flight_review", start_date)

        


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
            return "NEVER"

        elif checkride_date and not refresher_date:
            start_date = checkride_date

        elif refresher_date and not checkride_date:
            start_date = refresher_date

        elif checkride_date > refresher_date:
            start_date = checkride_date

        elif checkride_date < refresher_date:
            start_date = refresher_date

        ############

        return self.get_status("flight_instructor", start_date)









