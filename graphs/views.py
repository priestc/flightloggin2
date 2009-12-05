from django.utils.safestring import mark_safe

from logbook.constants import GRAPH_FIELDS, AGG_FIELDS, FIELD_TITLES
from annoying.decorators import render_to
from share.decorator import no_share

@no_share('other')
def linegraph_image(request, shared, display_user,
                    columns, dates=None, ext='png', rate=True):

    from linegraph import ProgressGraph
        
    if rate == 'rate':
        rate = True
        
    elif rate == 'norate':
        rate = False
        
    pg = ProgressGraph(display_user, columns, dates, rate)
    
    if ext == 'png':
        return pg.as_png()
    else:
        return pg.as_svg()

def bargraph_image(request, shared, display_user, column, func, agg):
    
    import bargraph as g
        
    if agg == 'person':
        Graph = g.PersonBarGraph
        
    elif agg == 'student':
        Graph = g.StudentBarGraph
    
    elif agg == 'captain':
        Graph = g.CaptainBarGraph
        
    elif agg == 'first_officer':
        Graph = g.FOBarGraph
        
    elif agg == 'instructor':
        Graph = g.InstructorBarGraph
    
    elif agg == 'type':
        Graph = g.PlaneTypeBarGraph
        
    elif agg == 'tailnumber':
        Graph = g.TailnumberBarGraph
        
    elif agg == 'manufacturer':
        Graph = g.ManufacturerBarGraph
    
    elif agg == 'category_class':
        Graph = g.CatClassBarGraph
        
    elif agg == 'year':
        Graph = g.YearBarGraph
        
    elif agg == 'month':
        Graph = g.MonthBarGraph
    
    elif agg == 'day_of_the_week':
        Graph = g.DOWBarGraph
    
    elif agg == 'month_year':
        Graph = g.MonthYearBarGraph
        
    else:
        assert False, "Agg not added to generator view"
    
    return Graph(display_user, column, agg, func).as_png()

###############################################################################

@no_share('other')
@render_to('linegraphs.html')
def linegraphs(request, shared, display_user):
    """the view function that renders the graph builder interface"""
    
    column_options = []
    for field in GRAPH_FIELDS:
        column_options.append("<option value=\"%s\">%s</option>" %
                                        (field, FIELD_TITLES[field] ) )
        
    column_options = mark_safe("\n".join(column_options))
    return locals()
    
###############################################################################

@no_share('other')
@render_to('bargraphs.html')
def bargraphs(request, shared, display_user):
    """the view function that renders the graph builder interface"""   
    
    column_options = []
    for field in ['total', 'route__total_line_all'] + AGG_FIELDS:
        column_options.append("<option value=\"%s\">%s</option>" %
                                        (field, FIELD_TITLES[field])
        )
    
    agg_options = []
    from constants import BAR_AGG_FIELDS
    for field in BAR_AGG_FIELDS:
        sys = field.split('By ')[1].lower().replace(" ",'_').replace('/','_')
        agg_options.append("<option value=\"%s\">%s</option>" %
                                (sys, field)
        )
        
    column_options = mark_safe("\n".join(column_options))
    agg_options = mark_safe("\n".join(agg_options))
    return locals()


def histogram(request):
    from histogram import Histogram
    b = Histogram()
    return b.as_png()
