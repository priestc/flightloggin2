import matplotlib
matplotlib.use('Agg')

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import rgb2hex

from django.db.models import Count

from graphs.image_formats import plot_png2, plot_svg

from is_shared import is_shared
from airport.models import Region, Airport

SMALL_STATES=['Rhode Island', 'Delaware', 'Maryland', 'Akaska',
              'Connecticut', 'Hawaii',]
              
ABBV = {'Rhode Island': "RI", 'Delaware': "DE", 'Maryland': "MD", 'Hawaii': "HI",
              'Connecticut': "CT", 'Alaska': "AK"}

def state_map(request, username, type_):
    shared, display_user = is_shared(request, username)
    
    if type_ == "colored":
        states = Region.objects.filter(airport__routebase__route__flight__user=display_user, country='US').values('name').distinct()
        
    elif type_ == "count":
        states = Region.objects.filter(airport__routebase__route__flight__user=display_user, country='US').values('name')\
                    .distinct().annotate(c=Count('name'))
                    
    elif type_ == "count-unique":
        states = Region.objects.filter(airport__in=Airport.objects.filter(routebase__route__flight__user=display_user, country="US")\
                    .distinct()).values('name').annotate(c=Count('airport__region'))
    else:
        assert False
                    
    new_dict = {}                
    for state in states:
        new_dict.update({state.get('name'): state.get('c', 1)})

    return drawl_state_map(new_dict)


@plot_png2
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
    max_ = max(states_to_plot.values())
    for i,seg in enumerate(m.states):
        statename = m.states_info[i]['NAME']
        
        if statename in states_to_plot:
            c = states_to_plot[statename]
            color = cmap(1.-np.sqrt((c-min_)/(max_-min_)))[:3]
            print color, c
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
                
            elif statename == "Alaska":
                plt.figtext(.83, .35, "AK", size="small", color=color)
                
            elif statename == "Hawaii":
                plt.figtext(.83, .35, "HI", size="small", color=color)
    
    #abbreviate, remove duplicates and make into a single string (small states, e.g. DE, MA, MD)
    #statetext= "\n".join([ABBV[s] for s in set(text)]) 
    #plt.figtext(.83, .2, statetext, size="small", color=color)
    
    #The unique state count text
    count = len(states_to_plot)
    plt.figtext(.15, .18, "%s\nUnique\nStates" % count, size="small")
            
    return fig
    
