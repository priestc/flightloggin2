from datetime import *
from dateutil.relativedelta import *

FAA_MEDICAL_DURATIONS = {                               #the time elapsed from the original exam date for each downgrade in calendar months
                                        "over": (6, 12, 48),
                                        "under": (12, 12, 60)
                                }


CURRENCY_DATA =
    {   0:      ("","",""),
                        1:      ("Flight Instructor",   "24", "cm", "30", "d"), # (name, duration, duration units, alert time, alert time units)
                        2:      ("Flight Review",       "24", "cm", "30", "d"),
                        3:      ("1st Class Medical"),
                        4:      ("2nd Class Medical"),
                        5:      ("3rd Class Medical"),

                        100:    ("FAA Landings",        "90", "d", "10", "d"),
                }

TODAY =                 date.today()



##############

class currency():
    id              =       0                       #the ref number for this currency routine
    title           =       CURRENCY_DATA[id][0]    #human readable title
    status          =       3                       #ref number for status, 0=expired, 1=current, 2=almost, 3=never
    start_date      =       date(500,07,21)         #date of event currency is based from, eg date of 3rd to last landing
    expire_date     =       date(501,07,21)         #date that the currency expires
    expired_since   =       date(501,07,22)         #first day of expiration

    def get_status(self):
        """determine if the current date is before, after, or in the alert timeframe."""

        expire_time     =       CURRENCY_DATA[self.id][1]
        expire_units    =       CURRENCY_DATA[self.id][2]

        if expire_units == "d":
            expire_delta    =       timedelta(days=expire_time)

        if expire_units == "m":
            expire_delta    =       timedelta(months=expire_time)

        if expire_units == "y":
            expire_delta    =       timedelta(years=expire_time)

        if expire_units == "cm":        #calendar months
            expire_delta    =       relativedelta(months=+expire_time + 1).replace(day=1) + relativedelta(days=-1)

        ###############################################################

        alert_time              =       CURRENCY_DATA[self.id][3]
        alert_units             =       CURRENCY_DATA[self.id][4]

        if alert_units == "d":
            alert_delta     =       timedelta(days=alert_time)

        if alert_units == "m":
            alert_delta     =       timedelta(months=alert_time)

        if alert_units == "y":
            alert_delta     =       timedelta(years=alert_time)

        if alert_units == "cm": #calendar months
            alert_delta     =       relativedelta(months=+expire_time + 1).replace(day=1) + relativedelta(days=-1)

        ####

        if self.id > 100:                                                               # landing currencies
            self.expire_date = self.start_date + relativedelta(days=+expire_time)
        else:
            self.expire_date = self.start_date + expire_delta

        ####

        if TODAY > expire_date:                                 #today is later than expire date, EXPIRED
            self.status = 0

        elif TODAY < expire_date and TODAY > alert_delta:       #today is later than alert, but not past expired date, ALERT
            self.status = 2

        elif TODAY < expire_date and TODAY < alert_delta:       #today is before expire date, and before alert date, CURRENT
            self.status = 1



        #if expire_date > TODAY + alert_delta:          #
        #       self.status = 1

        #if expire_date < TODAY + alert_delta:
        #       self.status = 2

        #if expire_date < TODAY:
        #       status = 0
        #       self.expire_date += relativedelta(days=+1)

        return

##############

class FAA_flight_review(currency):

    id = 2

    def determine(self):

        try:
            checkride_date = Flight.objects.filter(user=self.user, pilot_checkride=True).values_list("date", flat=True).reverse()[0]
        except:
            checkride_date = None

        try:
            fr_date = Flight.objects.filter(user=self.user, flight_review=True).values_list("date", flat=True).reverse()[0]
        except:
            fr_date = None

        ############

        if fr_date == None and checkride_date == None:                          # no checkrides nor flight reviews in database
            return

        elif fr_date == None and not checkride_date == None:                    #no flight review, but a pilot checkride, use the checkride date
            self.start_date = checkride_date

        elif checkride_date == None and not fr_date == None:                    #no checkride, but there is a flight review, use the flight review date
            self.start_date = fr_date

        elif checkride_date > fr_date:                                          #if there are both checkrides and flight reviews, use the one with the latest date
            self.start_date = checkride_date

        elif checkride_date < fr_date:
            self.start_date = fr_date

        ################################################################################

        self.get_status()

        return


class FAA_flight_instructor(currency):

    id = 1

    def determine(self):
        try:
            checkride_date = Flight.objects.filter(user=self.user, cfi_checkride=True).values_list("date", flat=True).reverse()[0]
        except:
            checkride_date = None

        try:
            refresher_date = NonFlight.objects.filter(user=self.user, non_flying=4).values_list("date", flat=True).reverse()[0]
        except:
            refresher_date = None

        ############

        if refresher_date == None and checkride_date == None:           # no checkrides nor flight reviews in database, return "never"
            return

        elif refresher_date == None and not checkride_date == None:
            self.start_date = checkride_date

        elif checkride_date == None and not refresher_date == None:
            self.start_date = refresher_date

        elif checkride_date > refresher_date:
            self.start_date = checkride_date

        elif checkride_date < refresher_date:
            self.start_date = refresher_date

        ############

        self.get_status()

        return
