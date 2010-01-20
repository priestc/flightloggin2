import datetime
import numpy as np

from django.utils.dateformat import format as dj_date_format

from graphs.image_formats import plot_png, plot_svg, plot_png2, plot_svg2

class StatsGraph(object):
    
    def __init__(self, val, rate=True):
        
        #create the figure instance
        from matplotlib.figure import Figure
        self.fig = Figure()
        
        from models import StatDB
        self.x = StatDB.objects.values_list('dt', flat=True).order_by('-dt')
        self.y = StatDB.objects.values_list(val, flat=True).order_by('-dt')
        
        print self.x, self.y
        
    def output(self):
        ax = self.fig.add_subplot(111)
        ax.plot(self.x,
                self.y,
                'red',
                lw=2)
                
        from graphs.format_ticks import format_line_ticks
        
        x = list(self.x)
        
        range_ = x[-1] - x[0]
           
        format_line_ticks(ax, 0.5)
        
        return self.fig
    
    def as_png(self):
        return plot_png(self.output)()
