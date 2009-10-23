from logbook.constants import *
from classes import ProgressGraph
from annoying.decorators import render_to

def graph_image(request, shared, display_user, columns, dates=None, ext='png'):
    
    pg = ProgressGraph(display_user, columns, dates)
    
    if ext == 'png':
        return pg.as_png()
    else:
        return pg.as_svg()

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
