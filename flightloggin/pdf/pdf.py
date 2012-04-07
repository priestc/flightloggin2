import datetime
from django.utils.dateformat import format

from django.template.loader import get_template
from django.http import HttpResponse
from django.template import Context

from flightloggin.logbook.models import Flight
from flightloggin.logbook.constants import FIELD_ABBV

from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Table, TableStyle, Paragraph, SimpleDocTemplate
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import landscape, letter

class PDF(object):
    
    PRINT_FIELDS = ('date', 'plane', 'route', 'total_s', 'pic', 'sic', 'solo', 
                    'act_inst', 'sim_inst', 'act_inst','xc','night','day_l',
                    'night_l','person', 'r_remarks')
                    
    def __init__(self, user):
        
        self.s_date = format(datetime.date.today(), 'Y-m-d')
        self.f_date = format(datetime.date.today(), 'l, M d, Y')
        
        self.user = user
    
        self.flights = Flight.objects\
                             .user(user)\
                             .order_by('date')\
                             .select_related()
                             
        cd = 'attachment; filename=logbook{0}.pdf'.format(self.s_date)
        self.response = HttpResponse(mimetype='application/pdf')
        self.response['Content-Disposition'] = cd
        
        self.doc = SimpleDocTemplate(self.response,
                                     pagesize=landscape(letter), 
                                     showBoundary=1,
                                     leftMargin=inch/4,
                                     rightMargin=inch/4,
                                     topMargin=inch/4,
                                     bottomMargin=inch/4,
                                     title="FlightLogg.in Logbook",
                                     author="FlightLogg.in")
                                     
        
    def define_style(self):
        """
        Define the styles that the rendered PDF will have
        """
        
        from reportlab.lib import colors
        
        self.styles = getSampleStyleSheet()
        
        self.ts = TableStyle([
                 ('FONTSIZE',       (0,0), (-1,-1), 4),
                 ('ALIGN',          (0,0), (-2,-1), 'CENTER'),
                 ('VALIGN',         (0,0), (-1,-1), 'TOP'),
                 ('ALIGN',          (0,-1),(-1,-1), 'LEFT'),
                 ('LEFTPADDING',    (0,0), (-1,-1), 1),
                 ('RIGHTPADDING',   (0,0), (-1,-1), 1),
                 ('TOPPADDING',     (0,0), (-1,-1), 1),
                 ('BOTTOMPADDING',  (0,0), (-1,-1), 1),
                 ('ROWBACKGROUNDS', (0,0), (0,-1),  ['#FFFF00']),
                 ('ROWBACKGROUNDS', (0,0), (-1,-1), ['#DDFFEE', '#FFFFFF']),
                 ('INNERGRID',      (0,0), (-1,-1), 0.25, colors.gray),
                 ('BOX',            (0,0), (-1,-1), 0.25, colors.gray),
                ])
    
    def make_elements(self):
        """
        Returns a list of all elements that will be rendered onto the document
        """
        
        self.define_style()
        
        heading_style = self.styles['Heading1']
        sub_heading_style = self.styles['Normal']
        
        real_name = self.user.get_profile().real_name
        name = real_name or self.user.username
        
        elements = []
        
        big_heading = Paragraph("{0}'s Logbook".format(name), heading_style)
        sub_heading = Paragraph(self.f_date, sub_heading_style)
        
        elements.append(big_heading)
        elements.append(sub_heading)
        
        elements += self.construct_rows()
        
        return elements
        
    def construct_rows(self):
        """
        Create the table elements with the user's flight data
        """
        
        elements = []
        
        rows = self.flights.count() + 1  #+1 because of the header
        header = [FIELD_ABBV[f] for f in self.PRINT_FIELDS]
        data = [header,]
        for f in self.flights:
            subdata = []
            for field in self.PRINT_FIELDS:
                subdata.append(f.column(field))
            data.append(subdata)
         
        # Create the table with the necessary style, and add it to the
        # elements list.
        table = Table(data,
                      rowHeights=rows*[0.10*inch],
                      style=self.ts,
                      repeatRows=1)
        
        elements.append(table)
        
        return elements
    
    def as_response(self):
        elements = self.make_elements()
        self.doc.build(elements)
        return self.response
        
