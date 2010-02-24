import datetime
import re

from dateutil.relativedelta import *

def minus_alert(alert_time, expire):
    try:
        number, unit = re.match("^(\d+)([a-z]+)$", alert_time).groups()
    except:
        raise ValueError("FL: Invalid unit formatting")
    
    number = int(number)
        
    if unit == "d":
        return expire - datetime.timedelta(days=number)
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
        return datetime.timedelta(days=number) + start
        
    elif unit == "m":
        return datetime.timedelta(months=number) + start

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
   
    def __init__(self, user, today=None):
        self.user = user
        
        self.start_date = None
        self.end_date = None
        self.status = None
        
        if not today:
            self.TODAY = datetime.date.today()
            
        try:
            self.calculate()
        except:
            pass
    
    def _determine(self, method, start_date, as_of=None):
        """
        Determine if the current date is before, after,
        or in the expire timeframe, or the alert timeframe.
        """
        
        if not start_date:
            return ("NEVER", None)
        
        #get the alert and expire times based on the master dict
        expire_time   =   self.CURRENCY_DATA[method][0]
        alert_time    =   self.CURRENCY_DATA[method][1]
        
        expire_date = get_date(expire_time, start_date)
        alert_date = minus_alert(alert_time, expire_date)
        
        if not as_of:
            as_of = self.TODAY

        #today is later than expire date, EXPIRED
        if as_of > expire_date:
            return ("EXPIRED", expire_date)
        
        #today is later than alert, but not past expired date, ALERT
        elif as_of <= expire_date and as_of >= alert_date:
            return ("ALERT", expire_date)
        
        #today is before expire date, and before alert date, CURRENT
        elif as_of <= expire_date and as_of < alert_date:
            return ("CURRENT", expire_date)
        
        else:
            assert False, "Greater than / less than signs off"
    
    def relevent(self):
        """
        If the user's status for this currency is long expired, don't even
        bother displaying it.
        """
        
        if not self.status:
            self.calculate()
        
        if self.status == "EXPIRED":
            return True
            
    def latest(self, *args):
        """return the latest date"""
        dates = []
        for arg in args:
            if arg: dates.append(arg)
        
        #if theres only one date, return it
        if len(dates) == 1:
            return dates[0]
        elif len(dates) == 0:
            return None
        
        #there are more than one date, return the highest
        return max(*dates)
    
    def days(self, item):
        """
        Find out how many days have lapsed since the end date
        (or how many days /until/ the end date)
        """
        
        status = getattr(self, "%s_status" % item, False)
        end = getattr(self, "%s_end" % item, False)
        
        days = None
        if status != "NEVER":
            days = str(abs(datetime.date.today() - end).days)
        
        setattr(self, '%s_days' % item, days)




