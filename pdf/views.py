import datetime
from django.utils.dateformat import format as dj_date_format

from annoying.decorators import render_to
from django.template.loader import get_template
from django.http import HttpResponse
from django.template import Context

from logbook.models import Flight
from logbook.constants import FIELD_ABBV

def pdf(request, display_user, shared):
    from reportlab.lib.styles import getSampleStyleSheet
    from reportlab.platypus import Table, TableStyle, Paragraph, SimpleDocTemplate
    from reportlab.lib.units import inch
    from reportlab.lib import colors
    from reportlab.lib.pagesizes import landscape, letter

    s_date = dj_date_format(datetime.date.today(), 'Y-m-d')
    f_date = dj_date_format(datetime.date.today(), 'l, M d, Y')
    
    response = HttpResponse(mimetype='application/pdf')
    response['Content-Disposition'] = 'attachment; filename=logbook%s.pdf' % s_date
    elements = []
    styles = getSampleStyleSheet()
    doc = SimpleDocTemplate(response, pagesize=landscape(letter), showBoundary=1,
                            leftMargin=inch/4, rightMargin=inch/4,
                            topMargin=inch/4, bottomMargin=inch/4,
                            title="FlightLogg.in Logbook",
                            author="FlightLogg.in")
     
    try:
        name = display_user.get_profile().username
    except:
        name = display_user

    elements.append(Paragraph("%s's Logbook" % name, styles['Heading1']))
    elements.append(Paragraph(f_date, styles['Normal']))
    
    print_fields = ('date', 'plane', 'route', 'total_s', 'pic', 'sic', 'solo', 
                    'act_inst', 'sim_inst', 'act_inst','xc','night','day_l',
                    'night_l','person', 'r_remarks')
                    
    flights = Flight.objects.filter(user=display_user).select_related()
    rows = flights.count() + 1  #+1 because of the header
    header = [FIELD_ABBV[f] for f in print_fields]
    data = [header,]
    for f in flights:
        subdata = []
        for field in print_fields:
            subdata.append(f.column(field))
        data.append(subdata)
        
    ts = TableStyle([('FONTSIZE',       (0,0), (-1,-1), 4),
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
     
    # Create the table with the necessary style, and add it to the
    # elements list.
    table = Table(data, rowHeights=rows*[0.10*inch], style=ts, repeatRows=1)
    
    
    
    elements.append(table)
     
    doc.build(elements)
    return response
