import re
import datetime

from django.db.models import Q

from flightloggin.plane.models import Plane
from logbook.models import Flight
from flightloggin.records.models import NonFlight

from currency import Currency

class FAA_Landing(Currency):
    
    CURRENCY_DATA = {
        "landings":            ("90d", "10d"),
    }
    
    def __init__(self, *args, **kwargs):
        self.item = kwargs.pop('item')
        self.qs = None
        self.tail = False
        self.cat_class = None
        super(FAA_Landing, self).__init__(*args, **kwargs)

    def figure_from_item(self):
        """
        split up the string 'item' value into three variables:
        type rating (bool), cat class (int), tailwheel (bool)
        """
        
        if type(self.item) is type(1):
            # its a category/class
            self.cat_class = self.item
            return None, self.item, False
        
        elif self.item.endswith('tw'):
            # its a tailwheel
            self.tail = True # for the currbox
            self.cat_class = int(self.item[:-2])
            return None, self.cat_class, True
        
        else:
            # it must be a type
            return self.item, None, None
    
    def eligible(self):
        """
        If the user has any flights in the type of plane, then return true
        """
        
        tr, cat_class, tail = self.figure_from_item()
        
        #starting queryset
        qs = Flight.objects.user(self.user)

            
        if cat_class:
            # filter by plane cat/class
            qs = qs.filter(plane__cat_class=cat_class, plane__retired=False)
        
        if tr:               
            # filter by type rating 
            qs = qs.filter(plane__type=tr)
        
        if tail:
            qs = qs.filter(plane__tags__icontains="TAILWHEEL")
 
        self.qs = qs.order_by('-date').values('date', 'day_l', 'night_l')
        
        return bool(self.qs)

    def calculate(self):
        """
        Returns the date of the third to last day or night landing,
        and whether or not it qualifies the user to be current
        """
        
        if not self.qs:
            self.eligible()
 
        night = self.qs.filter(night_l__gte=1)
        day = self.qs.filter(Q(day_l__gte=1) | Q(night_l__gte=1))
        
        self.calc_night(night)
        self.calc_day(day)
        
        return "day: %s" % self.day_status, "night: %s" % self.night_status
                
    def calc_day(self, qs):
        """
        Calculate day currency by finding the third to last night landing.
        """
        
        total = 0
        for flight in qs[:3]:
            total += flight.get('night_l',0) + flight.get('day_l',0)
            if total >= 3:
                self.day_start = flight['date']
                break;               
        
        if total < 3:
            self.day_status = 'NEVER'
            self.day_end = None
            self.day_start = None
        else:
            self.day_status, self.day_end = \
                                self._determine("landings", self.day_start)    
         
        self.days('day')
        
        return "day: %s" % self.day_status

    
    def calc_night(self, qs):
        """
        Calculate day currency by finding the third to last day or 
        night landing.
        """
        
        total = 0
        for flight in qs[:3]:
            total += flight.get('night_l',0)
            if total >= 3:
                self.night_start = flight['date']
                break;   
        
        if total < 3:
            self.night_status = 'NEVER'
            self.night_end = None
            self.night_start = None
        else:
            self.night_status, self.night_end = \
                                self._determine("landings", self.night_start)
                                
        self.days('night')
            
        return "night: %s" % self.night_status

class FAA_Certs(Currency):
    
    CURRENCY_DATA = {
        "flight_instructor":   ("24cm", "30d"),
        "flight_review":       ("24cm", "30d"),
    }
    
    def __init__(self, *args, **kwargs):
        self.cfi_start = None
        self.bfr_start = None
        super(FAA_Certs, self).__init__(*args, **kwargs)
    
    def eligible(self):
        """
        Returns true if there is either a cfi event or a bfr event in the
        user's logbook
        """
        return self.get_bfr() or self.get_cfi()
    
    def calculate(self):
        if not self.cfi_start and self.bfr_start:
            self.get_bfr()
            self.get_cfi()
        
        self.calc_bfr()
        self.calc_cfi()

    def get_cfi(self):
        
        checkride_date = None
        refresher_date = None
        
        try:
            checkride_date = Flight.objects\
                    .user(self.user)\
                    .filter(cfi_checkride=True)\
                    .values_list("date", flat=True)\
                    .latest()
            
        except Flight.DoesNotExist:
            pass
        
        #############################
        
        try:
            refresher_date = NonFlight.objects\
                    .user(self.user)\
                    .filter(non_flying=4)\
                    .values_list("date", flat=True)\
                    .latest()
                    
        except NonFlight.DoesNotExist:
            pass
        
        self.cfi_start = self.latest(refresher_date, checkride_date)
        
        return self.cfi_start

    def get_bfr(self):
        
        event_date = None
        flight_date = None
        
        try:
            # get latest checkride or flight review
            flight_date = Flight.objects\
                                .user(self.user)\
                                .filter(Q(pilot_checkride=True)
                                      | Q(flight_review=True))\
                                .values_list("date", flat=True)\
                                .latest()
            
        except Flight.DoesNotExist:
            pass
            
        try:
            ## try to get wings program
            event_date = NonFlight.objects\
                                  .user(self.user)\
                                  .filter(non_flying=6)\
                                  .values_list("date", flat=True)\
                                  .latest()

        except NonFlight.DoesNotExist:
            pass
            
        self.bfr_start = self.latest(event_date, flight_date)
        
        return self.bfr_start

    def calc_bfr(self):

        if not self.bfr_start:
            tup = ("NEVER", None)
        else:
            tup = self._determine("flight_review", self.bfr_start)
        
        self.bfr_status, self.bfr_end = tup
        
        self.days('bfr')
    
    def calc_cfi(self):

        if not self.cfi_start:
            tup = ("NEVER", None)
        else:
            tup = self._determine("flight_review", self.cfi_start)
        
        self.cfi_status, self.cfi_end = tup
        
        self.days('cfi')
    
###############################################################################

class FAA_Instrument(Currency):
    
    CURRENCY_DATA = {
        "instrument":          ("6cm", "30d"),
        "ipc":                 ("6cm", "30d"),
        "need_ipc":            ("6cm", "30d"),
    }
    
    def __init__(self, *args, **kwargs):
        if 'fake_class' not in kwargs.keys():
            raise RuntimeError('Instrument Currency class must be initialized with a fake class')
        
        self.fake_class = kwargs.pop('fake_class')
        super(FAA_Instrument, self).__init__(*args, **kwargs)
    
    def eligible(self):
        """
        Is the user eligible for this to be rendered? Do they have more than
        5 total approaches logged?
        """
        
        return Flight.objects.user(self.user)\
                     .pseudo_category(self.fake_class)\
                     .agg('app', float=True) > 5
    
    def calc_ipc(self):
        """
        Determine of the last IPC is still valid
        """
        
        try:
            self.ipc_start = Flight.objects\
                                   .user(self.user)\
                                   .filter(ipc=True)\
                                   .values_list("date", flat=True)\
                                   .latest()    
                                        
        except Flight.DoesNotExist:
            self.ipc_start = None
            
        # no ipc's in database, return "never"
        if not self.ipc_start:
            self.ipc_status = "NEVER"
            self.ipc_start = None
            self.ipc_end = None
        
        self.ipc_status, self.ipc_end =\
                self._determine("ipc", self.ipc_start)
        
        self.days('ipc')
        
    def calc_approaches(self):
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
                self.app_start = flight['date']
                break;
            
        self.app_status, self.app_end =\
                self._determine("instrument", self.app_start)
                
        self.days('app')
    
    def calc_ht(self):
        """
        Get the dates of the last 'holding' and 'tracking'
        """
        
        for ht in ('holding', 'tracking'):
            kwarg = {ht: True}
            
            try:
                start = Flight.objects\
                              .user(self.user)\
                              .pseudo_category(self.fake_class)\
                              .filter(**kwarg)\
                              .values_list('date', flat=True)\
                              .latest()
            
            except Flight.DoesNotExist:
                start = None
            
            status, end = self._determine("instrument", start)
        
            letter = ht[0]
        
            setattr(self, "%s_status" % letter, status)
            setattr(self, "%s_start" % letter, start)
            setattr(self, "%s_end" % letter, end)
            
            self.days(letter)
        
    def calculate(self):
        
        self.calc_ipc()
        self.calc_approaches()
        self.calc_ht()
        
        alert = False; expired = False
        for item in ("app", "h", "t"):
            
            st = getattr(self, "%s_status" % item)
            
            if st == "ALERT":
                alert = True
                
            if st == 'EXPIRED' or st == 'NEVER':
                expired = True
               
        if alert and not expired:
            #if any are alert and none are expired
            self.status = "ALERT"
            
        elif not expired:
            # if any none are expired
            self.status = "CURRENT"
        else:
            # if at least one is expired
            self.status = "EXPIRED"
            
        #ipc trumps all    
        if self.ipc_status == "CURRENT":
            self.status = "CURRENT"
            
        if self.ipc_status == "ALERT" and expired:
            self.status = "ALERT"
            
        if self.ipc_status == "ALERT" and not expired:
            self.status = "CURRENT"
            
        return self.status     
    
        
class FAA_Medical(Currency):

    CURRENCY_DATA = {
        "40":                  ("40y", "30d"),

        # the time elapsed from the original exam
        # date for each downgrade in calendar months
        "first_under":         ("12cm", "30d"),
        "second_under":        ("12cm", "30d"),
        "third_under":         ("60cm", "30d"),
        
        "first_over":          ("6cm", "30d"),
        "second_over":         ("12cm", "30d"),
        "third_over":          ("24cm", "30d"),
    }
    
    def eligible(self):
        return self.get_last_medical()
    
    def calculate_over_40(self):
        from profile.models import Profile
        try:
            ## try to get the user's DOB from their profile, if no profile
            # is made, assume they are over 40
            dob = Profile.get_for_user(self.user).dob
        except AttributeError, Profile.DoesNotExist:
            dob = datetime.date(1915,7,21)
        
        # find if they are over 40 based on their DOB
        status, end = self._determine("40", dob, as_of=self.exam_date)
        
        ## if this comes back expired, user is over 40
        self.over_40 = (status == "EXPIRED")
    
    def get_last_medical(self):
        try:
            last = NonFlight.objects\
                            .user(self.user)\
                            .filter(non_flying__in=[1,2,3])\
                            .latest()
                                    
            self.exam_class = last.non_flying
            self.exam_date = last.date
            
        except NonFlight.DoesNotExist:
            self.exam_class = None
            self.exam_date = None
            
        return self.exam_class
    
    def calculate(self):
        
        # don't want to calculate this twice
        if not self.exam_class:
            self.get_last_medical()
            
        self.calculate_over_40()
        
        self.calc_first_class()
        self.calc_second_class()
        self.calc_third_class()       


    def calc_first_class(self):
        
        if self.over_40:
            method = "first_over"
        else:
            method = "first_under"
            
        #if medical was not issued as a first, it can never be a first    
        if self.exam_class != 1:
            tup = ("NEVER", None)
        else:
            tup = self._determine(method, self.exam_date)
            
        self.first_status, self.first_end = tup
        
        self.days("first")

    def calc_second_class(self):
        
        if self.over_40:
            method = "second_over"
        else:
            method = "second_under"
            
        #if medical was issued as a third, it can never be a second
        if self.exam_class == 3:
            tup = ("NEVER", None)
        else:
            tup = self._determine(method, self.exam_date)
            
        self.second_status, self.second_end = tup
        
        self.days("second")
    
    
    def calc_third_class(self):
            
        if self.over_40:
            method = "third_over"
        else:
            method = "third_under"
            
        if not self.exam_class:
            tup = ("NEVER", None)
        else:   
            tup = self._determine(method, self.exam_date)
            
        self.third_status, self.third_end = tup

        self.days("third")





