from django.utils.safestring import mark_safe
from plane.constants import CATEGORY_CLASSES
from datetime import *
import math

class CurrBox(object):
    """takes the already calculated values of a currency state, and makes
       it into an HTML box, no database calls nor calculations are made here"""
    
    date_format = "Y-M-D"
    
    @classmethod
    def date_format(cls, format):
        cls.date_format = format
        
######################################
######################################

class LandCurrBox(CurrBox):
       
    cat_class = 0
   
    day = False
    night = False
    
    def __init__(self, cat_class=0, tr=None, tail=False):
    
        self.cat_class = cat_class
        
        if cat_class:
            self.title = CATEGORY_CLASSES[self.cat_class][1]
        
        elif tr:
            self.title = tr
            
        if tail:
            self.title += " Tailwheel"
        
    def render(self):
        
        lines = []
        lines.append("<div class='currbox'>")
            
        for time in ["day", "night"]:
            if not getattr(self, time)[0] == "NEVER":
                days_ago = abs((date.today() - getattr(self, time)[2]).days)
                current = bool(getattr(self, time)[0] == "ALERT" or getattr(self, time)[0] == "CURRENT")        # true if current
                class_name = getattr(self, time)[0].lower()
                start_date = str(getattr(self, time)[1])
                end_date = str(getattr(self, time)[2])
                
                lines.append("<div class='%s inner_currbox %s'>" % (class_name, time) )
                lines.append("<h3>%s %s</h3>" % (time.capitalize(), self.title) )
                lines.append("<p>Date of third-to-last landing: <strong>%s</strong><br>" % start_date )
                if current:
                    lines.append("Last day of currency: <strong>%s</strong> (%s Days remain)</p>" % (end_date, days_ago) )
                else:
                    lines.append("Last day of currency: <strong>%s</strong> (%s Days ago)</p>" % (end_date, days_ago) )
                
                lines.append("</div>")
            else:
            
                lines.append("<div class='expired inner_currbox %s'>" % time)
                lines.append("<h3>%s %s</h3>" % (time.capitalize(), self.title) )
                lines.append("<p>You do not have 3 landings</p>")
                lines.append("</div>")
                
        lines.append("</div>")         
        return mark_safe(" ".join(lines))
    
#################################################################
#################################################################
#################################################################

class MediCurrBox(CurrBox):

    first = None
    second = None
    third = None
    
    medi_issued = None

    def render(self):
        lines = []
        lines.append("<div class='currbox'>")
        
        word={1: "first", 2: "second", 3: "third"}
        
        for clas in [1, 2, 3]:
            ordinal = word[clas]
            if not getattr(self, ordinal)[0] == "NEVER":
                
                class_name = getattr(self, ordinal)[0].lower()
                start_date = str(getattr(self, ordinal)[1])
                end_date = str(getattr(self, ordinal)[2])
                current = bool(getattr(self, ordinal)[0] == "ALERT" or getattr(self, ordinal)[0] == "CURRENT")
                days_ago = abs((date.today() - getattr(self, ordinal)[2]).days)
                
                lines.append("<div class='medical_third %s'>" % class_name)
                lines.append("<h3>%s Class</h3>" % ordinal.capitalize() )
                
                if clas == self.medi_issued:
                    lines.append("<p>Date of exam: <strong>%s</strong><br>" % start_date)
                else:
                    lines.append("<br>")
                
                verbiage = "Ago"
                if current:
                    verbiage = "Remain"
                    
                lines.append("Last day of privileges: <strong>%s</strong><br>" % end_date)
                lines.append("(%s Days %s)</p>" % (days_ago, verbiage) )
                lines.append("</div>")
                
            else:
            
                lines.append("<div class='medical_third expired'>")
                lines.append("<h3>%s Class</h3>" % ordinal.capitalize() )
                #lines.append("<p>N/A</p>")
                lines.append("</div>")
        
        lines.append("</div>")
        return mark_safe(" ".join(lines))

#################################################################
#################################################################
#################################################################

class CertCurrBox(CurrBox):

    cfi = False
    bfr = False
        
    def __init__(self, cfi, bfr):
        self.cfi = cfi
        self.bfr = bfr

    def render(self):
        
        lines = []
        lines.append("<div class='currbox'>")
        
        title = {'cfi': "Flight Instructor", 'bfr': "Flight Review"}
        eq = {'cfi': "Flight Instructor Renewall", 'bfr': "Flight Review / Pilot Checkride"}
            
        for time in ["cfi", "bfr"]:
            if not getattr(self, time)[0] == "NEVER":
                days_ago = abs((date.today() - getattr(self, time)[2]).days)
                current = bool(getattr(self, time)[0] == "ALERT" or getattr(self, time)[0] == "CURRENT")        # true if current
                class_name = getattr(self, time)[0].lower()
                start_date = str(getattr(self, time)[1])
                end_date = str(getattr(self, time)[2])
                
                lines.append("<div class='%s inner_currbox %s'>" % (class_name, time) )
                lines.append("<h3>%s</h3>" % title[time] )
                lines.append("<p>Date of last %s: <strong>%s</strong><br>" % (eq[time], start_date) )
                
                if current:
                    lines.append("Last day of privileges: <strong>%s</strong> (%s Days remain)</p>" % (end_date, days_ago) )
                else:
                    lines.append("Last day of privileges: <strong>%s</strong> (%s Days ago)</p>" % (end_date, days_ago) )
                
                lines.append("</div>")
            else:
            
                lines.append("<div class='expired inner_currbox %s'>" % time)
                lines.append("<h3>%s</h3>" % title[time] )
                lines.append("<p>&nbsp;</p>")
                lines.append("</div>")
                
        lines.append("</div>")         
        return mark_safe(" ".join(lines)) 

#################################################################
#################################################################
#################################################################

class InstCurrBox(CurrBox):
    
    cat = None
    status = None
    start = None
    end = None
    
    def __init__(self, cat, currency):
        self.cat = cat
        self.status = currency[0]
        self.start_date = currency[1]
        self.end_date = currency[2]
    
    
    def render(self):
        lines = []
        lines.append("<div class='currbox'>")
        
        class_name = self.status.lower()
        days_ago = abs((date.today() - self.end_date).days)
        current = bool(self.status == "ALERT" or self.status == "CURRENT")        # true if current
        
        if current:
            
            lines.append("<div class='inner_currbox inst_curr %s'>" % class_name)
            lines.append("<h3>%s Instrument</h3>" % cat )
            lines.append("<p>Date of last qualifying event: <strong>%s</strong><br>" % self.start_date )
            
            if current:
                lines.append("Last day of privileges: <strong>%s</strong> (%s Days remain)</p>" % (self.end_date, days_ago) )
            else:
                lines.append("Last day of privileges: <strong>%s</strong> (%s Days ago)</p>" % (self.end_date, days_ago) )
            
            lines.append("</div>")
            
        else:
            lines.append("<div class='expired inner_currbox %s'>" % class_name)
            lines.append("<h3>%s Instrument</h3>" % self.cat )
            
        if self.status == 'NEED_IPC':
            lines.append("<p>Last day of currency: %s<br>(%s Days ago)<strong>You need an IPC</strong></p>" % (self.end_date, days_ago))
            lines.append("</div>")
        else:
            lines.append("</div>")
                
        lines.append("</div>")         
        return mark_safe(" ".join(lines))         



