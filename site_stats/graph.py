import datetime
import numpy as np

from django.utils.dateformat import format as dj_date_format

from graphs.image_formats import plot_png, plot_svg

class StatsGraph(object):
    
    def __init__(self, val, rate=True):
        
        #create the figure instance
        from matplotlib.figure import Figure
        self.fig = Figure()
        
        from models import StatDB
        self.title = val
        self.x = StatDB.objects.values_list('dt', flat=True).order_by('-dt')
        self.y = StatDB.objects.values_list(val, flat=True).order_by('-dt')
        
    def output(self):
        ax = self.fig.add_subplot(111)
        ax.plot(self.x,
                self.y,
                'red',
                lw=2)
                
        import time        
        from graphs.format_ticks import format_line_ticks
        from constants import STATS_TITLES
        ## 
        
        x = list(self.x)
        start = time.mktime(x[-1].timetuple())
        end = time.mktime(x[0].timetuple())
        range_ = (end - start) / (60.0 * 60.0 * 24 * 365)

        format_line_ticks(ax, range_)
        
        title = STATS_TITLES[self.title][0]
        unit = STATS_TITLES[self.title][1]
        
        self.fig.text(.5,.94, title, fontsize=18, ha='center')
        ax.set_ylabel(unit)
        ax.grid(True)
        
        return self.fig
    
    def as_png(self):
        return plot_png(self.output)()
    
    def as_svg(self):
        return plot_svg(self.output)()
