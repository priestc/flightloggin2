from django.utils.safestring import mark_safe
from plane.constants import CATEGORY_CLASSES
from datetime import *
import math

class CurrBox(object):
    cat_class = 0
    day = False
    night = False
    
    def __init__(self, cat_class=0, method="", date_format=""):
        self.cat_class = cat_class
        self.method = method
        self.date_format = date_format
        
    def render(self):
        
        lines = []
        lines.append("<div class='currbox'>")
        
        if self.method == "landings":
            
            for time in ["day", "night"]:
                if not getattr(self, time)[0] == "NEVER":
                    days_ago = abs((date.today() - getattr(self, time)[2]).days)
                    current = bool(getattr(self, time)[0] == "ALERT" or getattr(self, time)[0] == "CURRENT")        # true if current
                    class_name = getattr(self, time)[0].lower()
                    start_date = str(getattr(self, time)[1])
                    end_date = str(getattr(self, time)[2])
                    (str(getattr(self, time)[2]), days_ago)
                    
                    lines.append("<div class='%s inner_currbox %s'>" % (class_name, time) )
                    lines.append("<h2>%s %s</h2>" % (time.capitalize(), CATEGORY_CLASSES[self.cat_class][1]) )
                    lines.append("<p>Date of third-to-last landing: <strong>%s</strong><br>" % start_date )
                    if current:
                        lines.append("Last day of currency: <strong>%s</strong> (%s Days from now)</p>" % (end_date, days_ago) )
                    else:
                        lines.append("Last day of currency: <strong>%s</strong> (%s Days ago)</p>" % (end_date, days_ago) )
                    
                    lines.append("</div>")
                else:
                
                    lines.append("<div class='expired inner_currbox %s'>" % time)
                    lines.append("<h2>%s %s</h2>" % (time.capitalize(), CATEGORY_CLASSES[self.cat_class][1]) )
                    lines.append("<p>You do not have 3 landings</p>")
                    lines.append("</div>")
            
        lines.append("</div>")
        
        
        
        return mark_safe(" ".join(lines))
        #return "dfdf"
