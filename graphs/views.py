from logbook.constants import *
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

def bargraph_image(request, shared, display_user, column, agg, ext='png'):
    
    from bargraph import *
    
    if agg == 'cat_class':
        bg = CatClassBarGraph(display_user, column)
        
    if agg == 'person':
        bg = PersonBarGraph(display_user, column)
        
    if agg == 'student':
        bg = StudentBarGraph(display_user, column)
    
    if agg == 'captain':
        bg = CaptainBarGraph(display_user, column)
        
    if agg == 'fo':
        bg = FOBarGraph(display_user, column)
        
    if agg == 'instructor':
        bg = InstructorBarGraph(display_user, column)
    
    if agg == 'type':
        bg = PlaneTypeBarGraph(display_user, column)
        
    if agg == 'tailnumber':
        bg = TailnumberBarGraph(display_user, column)
    
    return bg.as_png()

###############################################################################

@render_to('graphs.html')
def graphs(request, shared, display_user):
    """the view function that renders the graph builder interface"""   
    
    column_options = []
    for field in GRAPH_FIELDS:
        column_options.append("<option value=\"%s\">%s</option>" %
                                        (field, FIELD_TITLES[field] ) )
        
    column_options = mark_safe("\n".join(column_options))
    return locals()
    
###############################################################################
###############################################################################
