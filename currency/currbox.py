from django.utils.safestring import mark_safe
from django.utils.dateformat import DateFormat
from plane.constants import CATEGORY_CLASSES
from datetime import *
import math

class CurrBox(object):
    """takes the already calculated values of a currency state, and makes
       it into an HTML box, no database calls nor calculations are made here"""
    
    date_format = "M d, Y"
    
    @classmethod
    def set_date_format(cls, format):
        cls.date_format = format
        
######################################
######################################

class LandCurrBox(CurrBox):
       
    cat_class = 0
   
    day = False
    night = False
    
    def __init__(self, cat_class=0, tr=None, tail=False):
    
        self.cat_class = cat_class

        self.title = ""        

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
                start_date = DateFormat(getattr(self, time)[1]).format(self.date_format)
                end_date = DateFormat(getattr(self, time)[2]).format(self.date_format)
                
                lines.append("<div class='%s inner_currbox %s'>" % (class_name, time) )
                lines.append("<h3>%s %s</h3>" % (time.capitalize(), self.title) )
                lines.append("<p>Date of third-to-last landing: <strong>%s</strong><br>" % start_date )
                if current:
                    lines.append("Last day of currency: <strong>%s</strong><br>(%s Days remain)</p>" % (end_date, days_ago) )
                else:
                    lines.append("Last day of currency: <strong>%s</strong><br>(%s Days ago)</p>" % (end_date, days_ago) )
                
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
        lines.append("<table class='currbox medical'>")
        
        word={1: "first", 2: "second", 3: "third"}
        
        for clas in [1, 2, 3]:
            ordinal = word[clas]
            if not getattr(self, ordinal)[0] == "NEVER":
                
                class_name = getattr(self, ordinal)[0].lower()
                start_date = DateFormat(getattr(self, ordinal)[1]).format(self.date_format)
                end_date =   DateFormat(getattr(self, ordinal)[2]).format(self.date_format)
                current = bool(getattr(self, ordinal)[0] == "ALERT" or getattr(self, ordinal)[0] == "CURRENT")
                days_ago = abs((date.today() - getattr(self, ordinal)[2]).days)
                
                lines.append("<td class='%s'>" % class_name)
                lines.append("<h3>%s Class</h3>" % ordinal.capitalize() )
                
                if clas == self.medi_issued:
                    lines.append("Date of exam: %s<br>" % start_date)
                else:
                    lines.append("<br>")
                
                verbiage = "Ago"
                if current:
                    verbiage = "Remain"
                    
                lines.append("Last day of privileges: %s<br>" % end_date)
                lines.append("(%s Days %s)<br>" % (days_ago, verbiage) )
                lines.append("</td>")
                
            else:
            
                lines.append("<td class='expired'>")
                lines.append("<h3>%s Class</h3>" % ordinal.capitalize() )
                lines.append("<br><br><br>")
                lines.append("</td>")
        
        lines.append("</table>")
        return mark_safe(" ".join(lines))

#################################################################
#################################################################
#################################################################

class CertCurrBox(CurrBox):

    cfi = False
    bfr = False
    
    do_cfi = True
    do_bfr = True
        
    def __init__(self, user):
        
        from FAA import FAA_Certs
        
        cert_object = FAA_Certs(user)
        
        self.cfi = cert_object.flight_instructor()
        self.bfr = cert_object.flight_review()
        
        
        if self.cfi[0] == "NEVER":
            self.do_cfi = False
            
        if self.bfr[0] == "NEVER":
            self.do_bfr = False

    def render(self):
        
        lines = []
        lines.append("<div class='currbox'>")
        
        title = {'cfi': "Flight Instructor", 'bfr': "Flight Review"}
        eq = {'cfi': "Flight Instructor Renewal", 'bfr': "Flight Review qualifying event"}
            
        for time in ["cfi", "bfr"]:
            if not getattr(self, time)[0] == "NEVER":
                days_ago = abs((date.today() - getattr(self, time)[2]).days)
                current = bool(getattr(self, time)[0] == "ALERT" or getattr(self, time)[0] == "CURRENT")        # true if current
                class_name = getattr(self, time)[0].lower()
                start_date = DateFormat(getattr(self, time)[1]).format(self.date_format)
                end_date =   DateFormat(getattr(self, time)[2]).format(self.date_format)
                
                lines.append("<div class='%s inner_currbox %s'>" % (class_name, time) )
                lines.append("<h3>%s</h3>" % title[time] )
                lines.append("<p>Date of last %s: <strong>%s</strong><br>" % (eq[time], start_date) )
                
                if current:
                    lines.append("Last day of privileges: <strong>%s</strong><br>(%s Days remain)</p>" % (end_date, days_ago) )
                else:
                    lines.append("Last day of privileges: <strong>%s</strong><br>(%s Days ago)</p>" % (end_date, days_ago) )
                
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
    
    def __init__(self, ci, fake_class):
        self.cat = fake_class
        self.status = ci.determine_overall_status()
        
        ##################################################
        
        self.six_start_date = ci.six_start
        self.six_end_date = ci.six_end
        self.six_status = ci.six_status
        
        if not self.six_status == "NEVER":
            six_days_ago = str(abs(date.today() - self.six_end_date).days)
            ed = DateFormat(self.six_end_date)\
                                        .format(self.date_format)
                                        
        if self.six_status == "EXPIRED":
            self.six_message = "Expired %s<br>(%s Days Ago)" % (ed, six_days_ago)
            self.six_class = self.six_status.lower()
            self.six_disp_date = DateFormat(self.six_start_date)\
                                        .format(self.date_format)
                                        
        elif self.six_status == "CURRENT" or self.six_status == "ALERT":
            self.six_message = "Last day of currency: %s<br>(%s Days Remain)" % (ed, six_days_ago)
            self.six_class = self.six_status.lower()
            self.six_disp_date = DateFormat(self.six_start_date)\
                                        .format(self.date_format)
        else:
            self.six_message = "Never<br><br>"
            self.six_disp_date = ""
            self.six_class = "expired"
            self.six_end_date = date(3000, 4, 4)
        
        ###############################################
    
        self.ipc_start_date = ci.ipc_start
        self.ipc_end_date = ci.ipc_end
        self.ipc_status = ci.ipc_status
        
        if not self.ipc_status == "NEVER":
            ipc_days_ago = str(abs(date.today() - self.ipc_end_date).days)
            ed = DateFormat(self.ipc_end_date)\
                                        .format(self.date_format)
                                        
        if self.ipc_status == "EXPIRED":
            self.ipc_message = "Expired %s<br>(%s Days Ago)" % (ed, ipc_days_ago)
            self.ipc_class = self.ipc_status.lower()
            self.ipc_disp_date = DateFormat(self.ipc_start_date)\
                                        .format(self.date_format)
                                        
        elif self.ipc_status == "CURRENT" or self.ipc_status == "ALERT":
            self.ipc_message = "Last day of currency: %s<br>(%s Days Remain)" % (ed, ipc_days_ago)   
            self.ipc_class = self.ipc_status.lower()
            self.ipc_disp_date = DateFormat(self.ipc_start_date)\
                                        .format(self.date_format)
        else:
            self.ipc_message = "Never<br><br>"
            self.ipc_disp_date = ""
            self.ipc_class = "expired"
            self.ipc_end_date = date(3000, 4, 4)
                                        
        ###############################################
        
        self.h_start_date = ci.h_start
        self.h_end_date = ci.h_end
        self.h_status = ci.h_status
        
        if not self.h_status == "NEVER":
            h_days_ago = str(abs(date.today() - self.h_end_date).days)
            ed = DateFormat(self.h_end_date)\
                                        .format(self.date_format)
                                        
        if self.h_status == "EXPIRED":
            self.h_message = "Expired %s<br>(%s Days Ago)" % (ed, h_days_ago)
            self.h_class = self.h_status.lower()
            self.h_disp_date = DateFormat(self.h_start_date)\
                                        .format(self.date_format)
                                        
        elif self.h_status == "CURRENT" or self.h_status == "ALERT":
            self.h_message = "Last day of currency: %s<br>(%s Days Remain)" % (ed, h_days_ago)    
            self.h_class = self.h_status.lower()
            self.h_disp_date = DateFormat(self.h_start_date)\
                                        .format(self.date_format)
        else:
            self.h_message = "Never<br><br>"
            self.h_disp_date = ""
            self.h_class = "expired"
            self.h_end_date = date(3000, 4, 4)
            
        ###############################################
    
        self.t_start_date = ci.t_start
        self.t_end_date = ci.t_end
        self.t_status = ci.t_status
        
        if not self.t_status == "NEVER":
            t_days_ago = str(abs(date.today() - self.t_end_date).days)
            ed = DateFormat(self.t_end_date)\
                                        .format(self.date_format)
        if self.t_status == "EXPIRED":
            self.t_message = "Expired %s<br>(%s Days Ago)" % (ed, t_days_ago)
            self.t_class = self.t_status.lower()
            self.t_disp_date = DateFormat(self.t_start_date)\
                                        .format(self.date_format)
                                        
        elif self.t_status == "CURRENT" or self.t_status == "ALERT":
            self.t_message = "Last day of currency: %s<br>(%s Days Remain)" % (ed, t_days_ago)
            self.t_class = self.t_status.lower()
            self.t_disp_date = DateFormat(self.t_start_date)\
                                        .format(self.date_format)
        else:
            self.t_message = "Never<br><br>"
            self.t_disp_date = ""
            self.t_class = "expired"        
            self.t_end_date = date(3000, 4, 4)
            
        ###############################################
        
#        first_end_date = min(self.h_end_date,
#                                    self.t_end_date, self.six_end_date,)
#        
#        self.days_ago = abs(date.today() - first_end_date).days
        
    def render(self):
        lines = []
        lines.append("<table class='currbox instrument'>")
        
        lines.append("<tr class='full_bar %s'>" % self.status.lower())
        lines.append("<td colspan='4'><strong>%s Instrument</strong></td>" % self.cat)
        lines.append("</td>")
        lines.append("</tr>")
        
        lines.append("<tr>")
        
        lines.append("<td class='%s'>" % self.six_class)
        lines.append("<strong>Sixth to last Approach:</strong><br>")
        lines.append(self.six_disp_date + "<br>")
        lines.append(self.six_message)
        lines.append("</td>")
        
        lines.append("<td class='%s'>" % self.h_class)
        lines.append("<strong>Last Hold:</strong><br>")
        lines.append(self.h_disp_date + "<br>")
        lines.append(self.h_message)
        lines.append("</td>")
        
        lines.append("<td class='%s'>" % self.t_class)
        lines.append("<strong>Last Tracking:</strong><br>")
        lines.append(self.t_disp_date + "<br>")
        lines.append(self.t_message)
        lines.append("</td>")
        
        lines.append("<td class='%s'>" % self.ipc_class)
        lines.append("<strong>Last IPC:</strong><br>")
        lines.append(self.ipc_disp_date + "<br>")
        lines.append(self.ipc_message)
        
        lines.append("</tr>")
        
        
        
        lines.append("</table>")
        
        return mark_safe(" ".join(lines))         



