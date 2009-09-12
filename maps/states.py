import matplotlib
matplotlib.use('Agg')

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap as Basemap
from matplotlib.colors import rgb2hex
from matplotlib.patches import Polygon

from graphs.image_formats import plot_png, plot_svg

#from matplotlib.figure import Figure

from is_shared import is_shared

@plot_svg
def state_map(request, username):
    shared, display_user = is_shared(request, username)
    
    fig = plt.figure()
    
    m = Basemap(llcrnrlon=-119,llcrnrlat=22,urcrnrlon=-64,urcrnrlat=49,
            projection='lcc',lat_1=33,lat_2=45,lon_0=-95)
            
    shp_info = m.readshapefile('/home/chris/Websites/flightloggin/maps/st99_d00','states',drawbounds=True)
    
    states = ['Florida', 'Ohio', ]
    return fig
    
    colors={}
    statenames=[]
    cmap = plt.cm.hot # use 'hot' colormap
    vmin = 0; vmax = 450 # set range.

    ax = plt.gca() # get current axes instance
    for nshape,seg in enumerate(m.states):
        # skip DC and Puerto Rico.
        if statenames[nshape] not in ['District of Columbia','Puerto Rico']:
            color = rgb2hex(colors[statenames[nshape]]) 
            poly = Polygon(seg,facecolor=color,edgecolor=color)
            ax.add_patch(poly)
    # draw meridians and parallels.
    m.drawparallels(np.arange(25,65,20),labels=[1,0,0,0])
    m.drawmeridians(np.arange(-120,-40,20),labels=[0,0,0,1])
    plt.title('Filling State Polygons by Population Density')
    plt.show()
    
    
