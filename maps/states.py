import matplotlib
matplotlib.use('Agg')

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import rgb2hex

from django.db.models import Count

from graphs.image_formats import plot_png2, plot_svg2
from airport.models import Region, Airport

def state_map_generator(request, shared, display_user, type_, ext):
    
    if ext == "png":
        func = plot_png2(state_map) #apply the correct decorator
        
    elif ext == "svg":
        func = plot_svg2(state_map)
        
    return func(request, display_user, type_, ext)

def state_map(request, user, type_, ext):
    
    if type_ == "colored":
        states = Region.objects.filter(airport__routebase__route__flight__user=user, country='US').values('name').distinct()
        
    elif type_ == "count":
        states = Region.objects.filter(airport__routebase__route__flight__user=user, country='US').values('name')\
                    .distinct().annotate(c=Count('name'))
                    
    elif type_ == "count-unique":
        states = Region.objects.filter(airport__in=Airport.objects.filter(routebase__route__flight__user=user, country="US")\
                    .distinct()).values('name').annotate(c=Count('airport__region'))
    else:
        assert False
                    
    states_to_plot = {}                
    for state in states:
        states_to_plot.update({state.get('name'): state.get('c', 1)})

    fig = drawl_state_map(states_to_plot)

    if type_ == "count-unique":
        count = sum(states_to_plot.values())
        label = "Airports"
    else:
        count = len(states_to_plot)
        label = "States"
        
    plt.figtext(.15, .18, "%s\nUnique\n%s" % (count, label), size="small")
    
    return fig

def drawl_state_map(states_to_plot):
    import settings
    from mpl_toolkits.basemap import Basemap as Basemap
    from matplotlib.patches import Polygon
    
    fig = plt.figure(figsize=(3.5, 2.5),)
    
    m = Basemap(llcrnrlon=-119,llcrnrlat=22,urcrnrlon=-64,urcrnrlat=49,
            projection='lcc',lat_1=33,lat_2=45,lon_0=-95)
            
    m.readshapefile(settings.PROJECT_PATH + '/maps/st99_d00','states',drawbounds=True)
    
    text = []
    ax = plt.gca() # get current axes instance
    
    c=['#009f0b','#d4ffd7']
    greencm=matplotlib.colors.LinearSegmentedColormap.from_list('mycm',c)
    
    cmap = greencm
    min_ = 0
    try:
        max_ = max(states_to_plot.values())
    except ValueError:
        max_ = 0
    ak=False
    hi=False    
    for i,seg in enumerate(m.states):
        statename = m.states_info[i]['NAME']
        
        if statename in states_to_plot:
            c = states_to_plot[statename]
            color = cmap(1.-np.sqrt((c-min_)/(max_-min_)))[:3]
            poly = Polygon(seg,facecolor=color)
            ax.add_patch(poly)
            
            if statename == "Rhode Island":
                plt.figtext(.83, .5, "RI", size="small", color=color)
            
            elif statename == "Connecticut":
                plt.figtext(.83, .45, "CT", size="small", color=color)
                
            elif statename == "Delaware":
                plt.figtext(.83, .4, "DE", size="small", color=color)
                
            elif statename == "Maryland":
                plt.figtext(.83, .35, "MD", size="small", color=color)
                
            elif statename == "Alaska" and not ak:
                plt.figtext(.83, .30, "AK", size="small", color=color)
                ak=True
                
            elif statename == "Hawaii" and not hi:
                plt.figtext(.83, .25, "HI", size="small", color=color)
                hi=True
    return fig
    
