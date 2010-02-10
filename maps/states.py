import numpy as np

from mpl_toolkits.basemap import Basemap, cm
from matplotlib.colors import rgb2hex, LinearSegmentedColormap
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas

from django.db.models import Count
from airport.models import Region, Location

###############################################################################
###############################################################################
###############################################################################

class StateMap(object):
    
    def __init__(self, user, ext='png'):
        self.user = user
        self.ext = ext
        self.get_cmap()
        
        from matplotlib.figure import Figure
        self.fig = Figure(figsize=(3.5, 2.5),)
        
        self.canvas = FigureCanvas(self.fig)
        self.ax = self.fig.add_subplot(111)
        
        self.m = Basemap(llcrnrlon=-120,
                         llcrnrlat=20.8,
                         urcrnrlon=-61.5,
                         urcrnrlat=50.3,
                         projection='lcc',
                         lat_1=33,
                         lat_2=45,
                         lon_0=-95,
                         ax=self.ax)
        
    def as_response(self):
        """
        Returns a HttpResponse containing the png or svg file.
        """
        
        self.plot()
        
        if self.ext == "png":
            mime = "image/png"
        else:
            mime = "image/svg+xml"
        
        from django.http import HttpResponse
        response = HttpResponse(mimetype=mime)
        
        self.fig.savefig(response,
                    format=self.ext,
                    bbox_inches="tight",
                    pad_inches=-.1,
                    edgecolor="white",
                    transparent=True)
                    
        return response
        
    def get_data(self):
        raise NotImplementedError

    def plot(self):
        """ Plot the states, and then make the labels
        """     
        
        states_to_plot = {}   
        qs = self.get_data()
        
        for state in qs:
            states_to_plot.update({state.get('name'): state.get('c', 1)})

        self.draw_state_map(states_to_plot)

        count = self.get_disp_count(states_to_plot)
            
        self.fig.text(.16,
                      .18,
                      "%s\nUnique\n%s" % (count, self.label),
                      size="small")

    def draw_state_map(self, states_to_plot):
        from matplotlib.patches import Polygon
        import settings
        
        import os
        path = os.path.join(settings.PROJECT_PATH, 'maps', 'st99_d00')
        self.m.readshapefile(path, 'states', drawbounds=True)

        text = []
        ax = self.fig.gca()

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
            
            colorize_state = statename in states_to_plot
            
            if colorize_state:
                c = float(states_to_plot[statename])
                val = np.sqrt( (c - min_) / (max_ - min_) )
                color = self.cmap(val)[:3]
            else:
                color = "white"    
            
            poly = Polygon(seg,facecolor=color)
            ax.add_patch(poly)
            
            if colorize_state:  
                over = .815
                
                if statename == "Rhode Island" and not ri:
                    self.fig.text(over, .5, "RI", size="small", color=color)
                    ri=True
                
                elif statename == "Connecticut" and not ct:
                    self.fig.text(over, .45, "CT", size="small", color=color)
                    ct=True
                    
                elif statename == "Delaware" and not de:
                    self.fig.text(over, .4, "DE", size="small", color=color)
                    de=True
                    
                elif statename == "Maryland" and not md:
                    self.fig.text(over, .35, "MD", size="small", color=color)
                    md=True
                    
                elif statename == "Alaska" and not ak:
                    self.fig.text(over, .3, "AK", size="small", color=color)
                    ak=True
                    
                elif statename == "Hawaii" and not hi:
                    self.fig.text(over, .25, "HI", size="small", color=color)
                    hi=True
                    
                elif statename == "District of Columbia" and not dc:
                    self.fig.text(over, .2, "DC", size="small", color=color)
                    dc=True
    
###############################################################################
    
class UniqueStateMap(StateMap):
    label = "Airports"
    
    def get_data(self):
        
        # all points in the USA connected to the user
        all_points = Location.objects\
                             .user(self.user)\
                             .filter(country="US")\
                             .distinct()

        
        return Region.objects\
                     .filter(location__in=all_points)\
                     .values('name')\
                     .annotate(c=Count('location__region'))
    
    def get_cmap(self):
        c=['#3342C1','#C1333B']
        self.cmap = LinearSegmentedColormap.from_list('mycm',c)
    
    def get_disp_count(self, stp):
        """stp = states to plot, a dict of all states and their values"""
        return sum(stp.values())
        

class FlatStateMap(StateMap):
    label = "States"
    
    def get_data(self):
        return Region.objects\
                     .user(self.user)\
                     .filter(country='US')\
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
        return Region.objects\
                     .user(self.user)\
                     .filter(country='US')\
                     .values('name')\
                     .distinct()\
                     .annotate(c=Count('code'))

    def get_cmap(self):
        c=['#3342C1','#C1333B']
        self.cmap = LinearSegmentedColormap.from_list('mycm',c)

    def get_disp_count(self, stp):
        return len(stp)
    
    
class RelativeStateMap(StateMap):
    label = "States"
    
    def get_data(self):
        
        overall_data = Region.objects\
                             .filter(country='US')\
                             .values('code')\
                             .annotate(c=Count('location'))\
                             .values('c','code')
        

        qs = Region.objects\
                   .user(self.user)\
                   .filter(country='US')\
                   .values('name')\
                   .distinct()\
                   .annotate(c=Count('code')) 

        ret = {}
        for key,q in qs.items():
            ret.update({key: overall_totals[key] / q[key]})
            
        return ret
            
    def get_cmap(self):
        self.cmap = cm.GMT_seis_r

    def get_disp_count(self, stp):
        return len(stp)   
