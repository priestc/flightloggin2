from django.utils.safestring import mark_safe
from django.utils.dateformat import format as dj_date_format

from constants import *

class LogbookRow(list):
    
    pk=0
    data = {}
    flight = []
    num_format = "decimal"
    date_format = "m-d-Y"
    
    @classmethod
    def set_formats(cls, df, nf):
        """Modifies the class so all instances have these date and number
        format attributes
        """
        cls.date_format = df
        cls.num_format = nf
        return cls
    
    def __init__(self, flight, columns):
        self.flight = flight
        self.pk = flight.pk
        self.route = flight.route
        self.columns = columns
        
        self.make_data()        
        self.make_proper_columns()
        
    def make_data(self):
        self.data = {}
        for field in DB_FIELDS:
            data = self.flight.column(field)
            
            if field == 'total' and data == "":
                self.data[field] = self.flight.column("sim")
            else:
                self.data[field] = data
        
    def make_proper_columns(self):
        for column in self.columns:
            
            if column == 'date':
                spans = self.get_data_spans()
                date = dj_date_format(self.flight.column('date'),
                                      self.date_format)
                title = "title=\"Date (click to so see more options)\""
                disp = """<a %s href="" id="f%s" class=\"popup_link\">%s%s</a>""" % \
                            (title, self.flight.id, date, spans)
            else:
                disp = self.flight.column(column, self.num_format)
                
            self.append( {"system": column,
                          "disp": mark_safe(disp),
                          "title": FIELD_TITLES[column]} )

    def get_data_spans(self):
        """
        Returns the <span>'s that hold the dta that is retrieved by the
        popup when editing a flight
        """
        out = []
        for field in DB_FIELDS:
            out.append('<span class="data_%s">%s</span>' % \
                            (field, self.data[field]))
        return "\n".join(out)

def to_minutes(flt):
    """converts decimal to HH:MM
    
    >>> to_minutes(.5452)
    '0:33'
    >>> to_minutes(2)
    2:00
    >>> to_minutes(1.2)
    '1:12'
    >>> to_minutes(-1.2)
    '-1:12'
    """
    
    value = str(flt + 0.0)
    h,d = value.split(".")
    minutes = float("0." + d) * 60
    return str(h) + ":" + "%02.f" % minutes
    
def from_minutes(value):
    """converts HH:MM to decimal
    
    >>> from_minutes("1:45")
    1.75
    >>> from_minutes("1:75")
    2.25
    >>> from_minutes("0:17")
    0.28333333333333333
    >>> from_minutes("-4:00")
    -4.0
    """
    
    hh,mm = value.split(":")
    mm = float(mm)
    hh = float(hh)
    return (mm / 60) + hh
