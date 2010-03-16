from django.utils.safestring import mark_safe
from annoying.decorators import render_to
from share.decorator import no_share

from logbook.constants import GRAPH_FIELDS, AGG_FIELDS, FIELD_TITLES
from constants import PLOT_COLORS
from linegraph import LogbookProgressGraph, LogbookPlot

@no_share('other')
def linegraph_image(request, columns, dates=None, ext='png',
                                                rate=True, spikes=True):

    if rate == 'rate':
        rate = True
        
    elif rate == 'norate':
        rate = False
        
    if spikes == '-spikes':
        spikes = True
        
    elif spikes == '-nospikes':
        spikes = False
    
    plots = []
    columns = columns.split('-')
    for column in columns:
        
        if len(columns) > 1:
            color = PLOT_COLORS[column]
        else:
            color = 'blue'
        
        p = LogbookPlot(
                user=request.display_user,
                column=column,
                range=dates,
                rate=rate,
                spikes=spikes,
                color=color,
            )
                       
        plots.append(p)
    
    pg = LogbookProgressGraph(plots)
    
    if ext == 'png':
        return pg.as_png()
    elif ext == 'svg':
        return pg.as_svg()
    else:
        assert False

##############################################################################

def bargraph_image(request, column, func, agg):
    
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
        
    elif agg == 'model':
        Graph = g.ModelBarGraph
        
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
    
    graph = Graph(request.display_user, column, agg, func)
    
    from profile.models import Profile
    graph.color_profile = Profile.get_for_user(request.display_user).style
    
    return graph.as_png()

###############################################################################

@no_share('other')
@render_to('linegraphs.html')
def linegraphs(request):
    """the view function that renders the linegraph builder interface"""
    
    column_options = []
    for field in GRAPH_FIELDS:
        column_options.append("<option value=\"%s\">%s</option>" %
                                        (field, FIELD_TITLES[field] ) )
        
    column_options = mark_safe("\n".join(column_options))
    return locals()
    
###############################################################################

@no_share('other')
@render_to('bargraphs.html')
def bargraphs(request):
    """the view function that renders the bargraph builder interface"""   
    from constants import BAR_AGG_FIELDS, BAR_FIELDS
    
    column_options = []
    for field in BAR_FIELDS:
        column_options.append("<option value=\"%s\">%s</option>" %
                                        (field, FIELD_TITLES[field])
        )
    
    agg_options = []
    
    for field in BAR_AGG_FIELDS:
        sys = field.split('By ')[1].lower().replace(" ",'_').replace('/','_')
        sel = ""
        if field == "By Type": sel = " selected=\"selected\"" #default
        agg_options.append("<option value=\"%s\"%s>%s</option>" %
                                (sys, sel, field)
        )
        
    column_options = mark_safe("\n".join(column_options))
    agg_options = mark_safe("\n".join(agg_options))
    return locals()
