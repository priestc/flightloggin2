from logbook.constants import * #FIXME
from annoying.decorators import render_to

from django.utils.safestring import mark_safe

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

def bargraph_image(request, shared, display_user, column, agg):
    
    from bargraph import *
    
    if agg == 'cat_class':
        bg = CatClassBarGraph(display_user, column)
        
    elif agg == 'person':
        bg = PersonBarGraph(display_user, column)
        
    elif agg == 'student':
        bg = StudentBarGraph(display_user, column)
    
    elif agg == 'captain':
        bg = CaptainBarGraph(display_user, column)
        
    elif agg == 'first_officer':
        bg = FOBarGraph(display_user, column)
        
    elif agg == 'instructor':
        bg = InstructorBarGraph(display_user, column)
    
    elif agg == 'type':
        bg = PlaneTypeBarGraph(display_user, column)
        
    elif agg == 'tailnumber':
        bg = TailnumberBarGraph(display_user, column)
        
    elif agg == 'manufacturer':
        bg = ManufacturerBarGraph(display_user, column)
    
    elif agg == 'category_class':
        bg = CatClassBarGraph(display_user, column)
        
    elif agg == 'year':
        bg = YearBarGraph(display_user, column)
        
    else:
        assert False
    
    return bg.as_png()

###############################################################################

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



