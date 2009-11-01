import matplotlib
matplotlib.use('Agg')

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap, cm
from matplotlib.colors import rgb2hex, LinearSegmentedColormap

from django.db.models import Count
from airport.models import Region, Location

def view(request, shared, display_user, type_, ext):
    if display_user.id == 1:
        display_user = None # unset user so it uses all users

    if type_ == 'unique':
        im = UniqueStateMap(display_user, ext)

    elif type_ == 'count':
        im = CountStateMap(display_user, ext)

    elif type_ == 'colored':
        im = FlatStateMap(display_user, ext)

    return im.output

###############################################################################
###############################################################################
###############################################################################

class StateMap(object):
    
    # the map, centered to the continental US
    m = Basemap(llcrnrlon=-119,llcrnrlat=22,urcrnrlon=-64,urcrnrlat=49,
                projection='lcc',lat_1=33,lat_2=45,lon_0=-95)
    
    
    def __init__(self, user, ext):
        self.user = user
        self.ext = ext
        self.get_cmap()
        
    @property
    def output(self):
        from graphs.image_formats import plot_png2, plot_svg2
        
        if self.ext == 'png':
            return plot_png2(self.plot)()
        
        if self.ext == 'svg':
            return plot_svg2(self.plot)()
        
    def get_data(self):
        raise NotImplementedError

    def plot(self):     
        states_to_plot = {}   
        qs = self.get_data()
        
        for state in qs:
            states_to_plot.update({state.get('name'): state.get('c', 1)})

        fig = self.drawl_state_map(states_to_plot)

        count = self.get_disp_count(states_to_plot)
            
        plt.figtext(.15,
                    .18,
                    "%s\nUnique\n%s" % (count, self.label),
                    size="small")
        
        return fig

    def drawl_state_map(self, states_to_plot):
        from matplotlib.patches import Polygon
        from airport.models import USStates
        import settings
        
        fig = plt.figure(frameon=False, figsize=(3.5, 2.5),)
        
        self.m.readshapefile(settings.PROJECT_PATH + '/maps/st99_d00',
                                'states',drawbounds=True)

        text = []
        ax = plt.gca() #fig.add_subplot(111, frameon=False, xticks=[], yticks=[])

        # get the min and max values for coloration
        try:
            min_ = 0
            max_ = max(states_to_plot.values())
        except ValueError:
            # queryset returned zero results for some reason
            min_ = 0
            max_ = 0
            
        ak, hi, de, md, ri, ct, dc = (False, ) * 7
        
        y=False
        for i,seg in enumerate(self.m.states):
            statename = self.m.states_info[i]['NAME']
            
            if statename in states_to_plot:
                c = float(states_to_plot[statename])
                val = np.sqrt((c-min_)/(max_-min_))
                color = self.cmap(val)[:3]
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
                    plt.figtext(.83, .3, "AK", size="small", color=color)
                    ak=True
                    
                elif statename == "Hawaii" and not hi:
                    plt.figtext(.83, .25, "HI", size="small", color=color)
                    hi=True
                    
                elif statename == "District of Columbia" and not dc:
                    plt.figtext(.83, .2, "DC", size="small", color=color)
                    dc=True
        return fig
    
###############################################################################
    
class UniqueStateMap(StateMap):
    label = "Airports"
    
    def get_data(self):
        
        if self.user:
            # all points in the USA connected to the user
            all_points = Location.objects\
              .filter(routebase__route__flight__user=self.user,country="US")\
              .distinct()
        else:
            #all points in the us connected to all users
            all_points = Location.objects\
              .filter(routebase__isnull=False, country="US")\
              .distinct()
        
        return Region.objects\
            .filter(location__in=all_points)\
            .values('name')\
            .annotate(c=Count('location__region'))
    
    def get_cmap(self):
        self.cmap = cm.GMT_seis_r
    
    def get_disp_count(self, stp):
        """stp = states to plot, a dict of all states and their values"""
        return sum(stp.values())
        

class FlatStateMap(StateMap):
    label = "States"
    
    def get_data(self):
        if self.user:
            return Region.objects\
                .filter(location__routebase__route__flight__user=self.user,
                    country='US')\
                .values('name')\
                .distinct()
        else:
            return Region.objects\
                .filter(location__routebase__isnull=False,
                    country='US')\
                .values('name')\
                .distinct()
            
    def get_cmap(self):
        c=['#FF00FF','#15AC1C']
        self.cmap = LinearSegmentedColormap.from_list('mycm',c)
        
    def get_disp_count(self, stp):
        return len(stp)


class CountStateMap(StateMap):
    label = "States"
    
    def get_data(self):
        if self.user: 
            return Region.objects\
                .filter(location__routebase__route__flight__user=self.user,
                    country='US')\
                .values('name')\
                .distinct().annotate(c=Count('code')) 
        else:
             return Region.objects\
                .filter(location__routebase__isnull=False,
                    country='US')\
                .values('name')\
                .distinct().annotate(c=Count('code')) 

    def get_cmap(self):
        self.cmap = cm.GMT_seis_r

    def get_disp_count(self, stp):
        return len(stp)





































    
