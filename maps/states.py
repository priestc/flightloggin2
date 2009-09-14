import matplotlib
matplotlib.use('Agg')

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import rgb2hex

from graphs.image_formats import plot_png2, plot_svg

#from matplotlib.figure import Figure

from is_shared import is_shared
from airport.models import Region

def state_map(request, username):
    shared, display_user = is_shared(request, username)
    
    states = Region.objects.filter(airport__routebase__route__flight__user=display_user, country='US').values_list('name', flat=True).distinct()
    
    return drawl_state_map(states)


@plot_png2
def drawl_state_map(states_to_plot):
    import settings
    from mpl_toolkits.basemap import Basemap as Basemap
    from matplotlib.patches import Polygon
    
    color="#24a153"
    
    small_states=['Rhode Island', 'Delaware', 'Maryland',
                  'Massachusetts', 'Connecticut',]
                  
    abbv = {'Rhode Island': "RI", 'Delaware': "DE", 'Maryland': "MD", 'Hawaii': "HI",
                  'Massachusetts': "MA", 'Connecticut': "CT", 'Alaska': "AK"}
        
    fig = plt.figure(figsize=(3.5, 2.5),)
    
    m = Basemap(llcrnrlon=-119,llcrnrlat=22,urcrnrlon=-64,urcrnrlat=49,
            projection='lcc',lat_1=33,lat_2=45,lon_0=-95)
            
    m.readshapefile(settings.PROJECT_PATH + '/maps/st99_d00','states',drawbounds=True)
    
    text = []
    ax = plt.gca() # get current axes instance
    for i,seg in enumerate(m.states):
        statename = m.states_info[i]['NAME']
        
        if statename in states_to_plot:
            poly = Polygon(seg,facecolor=color)
            ax.add_patch(poly)
            if statename in small_states:  #collect all small states
                text.append(statename)
    
    #abbreviate, remove duplicates and make into a single string (small states, e.g. DE, MA, MD
    statetext= "\n".join([abbv[s] for s in set(text)]) 
    plt.figtext(.83, .2, statetext, size="small", color=color)
    
    #The unique state count text
    count = len(states_to_plot)
    plt.figtext(.15, .18, "%s\nUnique\nStates" % count, size="small")
            
    return fig
    
    
