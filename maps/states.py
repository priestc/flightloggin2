import matplotlib
matplotlib.use('Agg')

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import rgb2hex

from django.db.models import Count
from airport.models import Region, Location

def view(request, shared, display_user, type_, ext):
    c = StateMap(display_user, type_, ext)
    return c.output

class StateMap(object):
    def __init__(self, user, type_, ext):
        self.user = user
        self.ext = ext
        self.type = type_
        self.qs = getattr(self, "get_%s_qs" % type_)
        
    @property
    def output(self):
        from graphs.image_formats import plot_png2, plot_svg2
        
        if self.ext == 'png':
            return plot_png2(self.plot)()
        
        if self.ext == 'svg':
            return plot_svg2(self.plot)()
    
    @property    
    def get_count_qs(self):
        return Region.objects\
            .filter(location__routebase__route__flight__user=self.user,
                country='US')\
            .values('name')\
            .distinct().annotate(c=Count('name'))
    
    @property                
    def get_unique_qs(self):
        return Region.objects\
            .filter(location__in=Location.objects\
              .filter(routebase__route__flight__user=self.user,country="US")\
              .distinct())\
            .values('name')\
            .annotate(c=Count('location__region'))
    
    @property       
    def get_colored_qs(self):
        return Region.objects\
            .filter(location__routebase__route__flight__user=self.user,
                country='US')\
            .values('name')\
            .distinct()
                    

    def plot(self):
                    
        states_to_plot = {}                
        for state in self.qs:
            states_to_plot.update({state.get('name'): state.get('c', 1)})

        fig = self.drawl_state_map(states_to_plot)

        if self.type == "count-unique":
            count = sum(states_to_plot.values())
            label = "Airports"
        else:
            count = len(states_to_plot)
            label = "States"
            
        plt.figtext(.15, .18, "%s\nUnique\n%s" % (count, label), size="small")
        
        return fig

    def drawl_state_map(self, states_to_plot):
        import settings
        from mpl_toolkits.basemap import Basemap
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
            
        ak, hi, de, md, ri, ct = False, False, False, False, False, False
        
        for i,seg in enumerate(m.states):
            statename = m.states_info[i]['NAME']
            
            if statename in states_to_plot:
                c = states_to_plot[statename]
                color = cmap(1.-np.sqrt((c-min_)/(max_-min_)))[:3]
                poly = Polygon(seg,facecolor=color)
                ax.add_patch(poly)
                
                if statename == "Rhode Island" and not ri:
                    plt.figtext(.83, .5, "RI", size="small", color=color)
                    ri=True
                
                elif statename == "Connecticut" and not ct:
                    plt.figtext(.83, .45, "CT", size="small", color=color)
                    ct=True
                    
                elif statename == "Delaware" and not de:
                    plt.figtext(.83, .4, "DE", size="small", color=color)
                    de=True
                    
                elif statename == "Maryland" and not md:
                    plt.figtext(.83, .35, "MD", size="small", color=color)
                    md=True
                    
                elif statename == "Alaska" and not ak:
                    plt.figtext(.83, .30, "AK", size="small", color=color)
                    ak=True
                    
                elif statename == "Hawaii" and not hi:
                    plt.figtext(.83, .25, "HI", size="small", color=color)
                    hi=True
        return fig
    
