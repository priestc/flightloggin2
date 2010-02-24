from django.utils.safestring import mark_safe

from plane.constants import CATEGORY_CLASSES
from datetime import *
import math

class CurrBox(object):
    """
    Takes the already calculated values of a currency state, and makes
    it into an HTML box, no database calls nor calculations are made here
    """
    
    date_format = "M d, Y"
    
    @classmethod
    def set_date_format(cls, format):
        cls.date_format = format
        
    def __init__(self, currency):
        self.currency = currency
        
    def df(self, date):
        """
        Format all dates into one format as defined by the dateformat variable
        """
        from django.utils.dateformat import format
        return format(date, self.date_format)
    
    def bottom_message(self, item):
        
        status = getattr(self.currency, "%s_status" % item)
        days = getattr(self.currency, "%s_days" % item)
        end = getattr(self.currency, "%s_end" % item)
        
        if status == "EXPIRED":
            ret = "Last day of currency: <strong>%s</strong><br>(%s Days ago)</p>"
        
        elif status == "NEVER":
            return "<p>You do not have %s</p>" % self.bottom_message_text
        
        elif status in ("CURRENT", "ALERT"):
            ret = "Last day of currency: <strong>%s</strong><br>(%s Days remain)</p>"
        
        return ret % (self.df(end), days)
    
    def top_message(self, item):
        
        status = getattr(self.currency, "%s_status" % item)
        start = getattr(self.currency, "%s_start" % item)
        
        if status == "NEVER":
            return ""
        
        return "<p>Date of %s: <strong>%s</strong><br>"\
                     % (self.top_message_text, self.df(start))
        
######################################
######################################

class LandCurrBox(CurrBox):
        
    top_message_text = "third-to-last landing"    
    bottom_message_text = "3 landings"
    
    def render(self):  
        
        if self.currency.cat_class:
            # get the name of the cat/class
            title = CATEGORY_CLASSES[self.currency.cat_class][1]
        else:
            # the title will be the type (which is in the item variable)
            title = self.currency.item
        
        if self.currency.tail:
            title += " Tailwheel"
        
        day_status = self.currency.day_status.lower()
        night_status = self.currency.night_status.lower()
        
        lines = [
            "<div class='currbox'>",
                "<div class='%s inner_currbox day'>" % day_status,
                    "<h3>%s Day</h3>" % title,
                    self.top_message('day'),
                    self.bottom_message('day'),
                "</div>",
                
                "<div class='%s inner_currbox night'>" % night_status,
                    "<h3>%s Night</h3>" % title,
                    self.top_message('night'),
                    self.bottom_message('night'),
                "</div>",
            "</div>"
        ]
        
        return mark_safe(" ".join(lines))
    
#################################################################
#################################################################
#################################################################

class MediCurrBox(CurrBox):
    
    def message(self, c):
        
        status = getattr(self.currency, "%s_status" % c)
        end = getattr(self.currency, "%s_end" % c)
        days = getattr(self.currency, "%s_days" % c)
        
        if status == 'NEVER':
            ## return two breaks to line the header up with the rest
            return "<br><br>"
        
        m = "Last day of privileges: %s" % self.df(end)
        
        if status in ('CURRENT', 'ALERT'):
            return m + "<br>(%s Days Remain)" % days
        else:
            return m + "<br>(%s Days Ago)" % days
    
    def date_of_exam(self, c):
        """
        If the medical was issued as the passed in class, then return a message
        saying when the medical exam took place.
        """
        
        if self.currency.exam_class == c:
            return "Date of exam: %s" % self.df(self.currency.exam_date)
    
        return ""
    
    def render(self):
        lines = [
            "<table class='currbox medical'>",
                "<tr>",
                
                    "<td class='%s'>" % self.currency.first_status.lower(),
                        "<h3>First Class</h3>",
                        self.date_of_exam(1),
                        "<br>",
                        self.message("first"),
                    "</td>",
                    
                    "<td class='%s'>" % self.currency.second_status.lower(),
                        "<h3>Second Class</h3>",
                        self.date_of_exam(2),
                        "<br>",
                        self.message("second"),
                    "</td>",
                    
                    "<td class='%s'>" % self.currency.third_status.lower(),
                        "<h3>Third Class</h3>",
                        self.date_of_exam(3),
                        "<br>",
                        self.message("third"),
                    "</td>",
                    
                "</tr>",
            "</table>",
        ]
        
        return mark_safe(" ".join(lines))

#################################################################
#################################################################
#################################################################

class CertsCurrBox(CurrBox):
    
    top_message_text = "renewal event"
    bottom_message_text = "any qualifying events"
        
    def render(self):
        
        cfi_status = self.currency.cfi_status.lower()
        bfr_status = self.currency.bfr_status.lower()
        
        lines = [
            "<div class='currbox'>",
                "<div class='%s inner_currbox day'>" % bfr_status,
                    "<h3>Flight Review</h3>",
                    self.top_message('bfr'),
                    self.bottom_message('bfr'),
                "</div>",
                
                "<div class='%s inner_currbox night'>" % cfi_status,
                    "<h3>Instructor Certificate</h3>",
                    self.top_message('cfi'),
                    self.bottom_message('cfi'),
                "</div>",
            "</div>"
        ]
        
        return mark_safe(" ".join(lines))

#################################################################
#################################################################
#################################################################

class InstCurrBox(CurrBox):
    
    def format_app(self):
        """
        Format all the approach display variables
        """
        
        status = self.currency.app_status
        end = self.currency.app_end
        start = self.currency.app_start
        days = self.currency.app_days
        
        if status == "EXPIRED":
            self.app_disp_date = self.df(start)
            self.app_message = "Expired %s<br>(%s Days Ago)"\
                    % (self.df(end), days)
                           
        elif status == "CURRENT" or status == "ALERT":
            self.app_disp_date = self.df(start)
            self.app_message = "Last day of currency: %s<br>(%s Days Remain)"\
                    % (self.df(end), days)
        else:
            self.app_message = "Never<br><br>"
            self.app_disp_date = ""

    def format_ipc(self):
        """
        Format all the ipc display variables
        """
    
        start = self.currency.ipc_start
        end = self.currency.ipc_end
        status = self.currency.ipc_status
        days = self.currency.ipc_days
        
        if status == "EXPIRED":
            self.ipc_disp_date = self.df(start)
            self.ipc_message = "Expired %s<br>(%s Days Ago)"\
                                    % (self.df(end), days)
                                        
        elif status == "CURRENT" or status == "ALERT":
            self.ipc_disp_date = self.df(start)
            self.ipc_message = "Last day of currency: %s<br>(%s Days Remain)"\
                                % (self.df(end), days)   
        else:
            self.ipc_message = "Never<br><br>"
            self.ipc_disp_date = ""
    
    def format_h(self):
        """
        Format all the h display variables
        """
    
        start = self.currency.h_start
        end = self.currency.h_end
        status = self.currency.h_status
        days = self.currency.h_days
        
        if status == "EXPIRED":
            self.h_disp_date = self.df(start)
            self.h_message = "Expired %s<br>(%s Days Ago)"\
                                 % (self.df(end), days)
                                        
        elif status == "CURRENT" or status == "ALERT":
            self.h_disp_date = self.df(start)
            self.h_message = "Last day of currency: %s<br>(%s Days Remain)"\
                                % (self.df(end), days)   
        else:
            self.h_message = "Never<br><br>"
            self.h_disp_date = ""
    
    def format_t(self):
        """
        Format all the t display variables
        """
    
        start = self.currency.t_start
        end = self.currency.t_end
        status = self.currency.t_status
        days = self.currency.t_days
        
        if status == "EXPIRED":
            self.t_disp_date = self.df(start)
            self.t_message = "Expired %s<br>(%s Days Ago)"\
                                % (self.df(end), days)
                                        
        elif status == "CURRENT" or status == "ALERT":
            self.t_disp_date = self.df(start)
            self.t_message = "Last day of currency: %s<br>(%s Days Remain)"\
                                % (self.df(end), days)   
        else:
            self.t_message = "Never<br><br>"
            self.t_disp_date = ""
        
    def render(self):
        
        self.format_app()
        self.format_h()
        self.format_t()
        self.format_ipc()
        
        import string
        cat = string.capwords(self.currency.fake_class.replace('_', ' '))
        
        lines = [
            "<table class='currbox instrument'>",
            
                "<tr class='full_bar %s'>" % self.currency.status.lower(),
                    "<td colspan='4'>",
                        "<strong>%s Instrument</strong>" % cat,
                    "</td>"
                "</tr>",
            
                "<tr>",
            
                    "<td class='%s'>" % self.currency.app_status.lower(),
                        "<strong>Sixth to last Approach:</strong>",
                        "<br>",
                        self.app_disp_date,
                        "<br>",
                        self.app_message,
                    "</td>",
            
                    "<td class='%s'>" % self.currency.h_status.lower(),
                        "<strong>Last Hold:</strong>",
                        "<br>",
                        self.h_disp_date,
                        "<br>",
                        self.h_message,
                    "</td>",
            
                    "<td class='%s'>" % self.currency.t_status.lower(),
                        "<strong>Last Tracking:</strong>",
                        "<br>",
                        self.t_disp_date,
                        "<br>",
                        self.t_message,
                    "</td>",
            
                    "<td class='%s'>" % self.currency.ipc_status.lower(),
                        "<strong>Last IPC:</strong>",
                        "<br>",
                        self.ipc_disp_date,
                        "<br>",
                        self.ipc_message,
                    "</td>",
            
                "</tr>",
            "</table>"
        ]
        
        return mark_safe(" ".join(lines))          



