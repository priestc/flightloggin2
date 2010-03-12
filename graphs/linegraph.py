import datetime

from django.utils.dateformat import format as dj_date_format

from image_formats import plot_png, plot_svg, plot_png2, plot_svg2
from logbook.constants import FIELD_TITLES

from main.mixins import NothingHereMixin

class ProgressGraph(NothingHereMixin):

    # the date format of the subtitle
    df = "F jS, Y"
    
    # the window for rate calculations
    r = 30

    def __init__(self, *args, **kwargs):
        from matplotlib.figure import Figure
        self.fig = Figure()
        self.rate = kwargs.pop('rate', False)
        
        r = kwargs.pop('range', False)
        
        if r:
            self.split_dates(r)
        else:
            self.end, self.start, self.year_range = (None,) * 3
            
    def split_dates(self, date_range):
        dates = date_range.split('-')
        s = dates[0]
        e = dates[1]
        
        # turn "2007.5.14" to "datetime.date(2007, 5, 14)"
        self.start = datetime.date(*[int(x) for x in s.split('.')])
        self.end   = datetime.date(*[int(x) for x in e.split('.')])
        self.year_range = (self.end-self.start).days / 365.0
        
        self.interval_start = self.start - datetime.timedelta(days=self.r)   
    
    def set_titles(self, title, subtitle):
        self.fig.text(.5,.94,title, fontsize=18, ha='center')
        self.fig.text(.5,.91,subtitle,fontsize=10,ha='center')
    
    def output(self):
        plots = self.get_plots()

        #add each plot to the figure
        for plot in plots:
            self.add_plot(plot)
            
        self.fig.gca().set_xlim(self.start, self.end)
        
        return self.fig
    
    def add_plot(self, plot):
        c = plot.kwargs['color']
        ax = self.fig.add_subplot(111)
        ax.plot(plot.x, plot.y, **plot.kwargs)
        ax.set_ylabel(plot.unit, color=c)
        
        for tl in ax.get_yticklabels():
                tl.set_color(c)
        
        if plot.do_rate:
            c = plot.rate_kwargs['color']
            ax2 = ax.twinx()
            ax2.plot(plot.rx, plot.ry, **plot.rate_kwargs)
            ax2.set_ylabel(plot.rate_unit, color=c)
            
            for tl in ax2.get_yticklabels():
                tl.set_color(c)
        
        from format_ticks import format_line_ticks    
        format_line_ticks(ax, self.year_range)
        ax.grid(True)
    
    @plot_png
    def as_png(self):
        try:
            return self.output()
        except self.EmptyLogbook:
            return self.NothingHereGraph
    
    @plot_png
    def as_svg(self):
        try:
            return self.output()
        except self.EmptyLogbook:
            return self.NothingHereGraph

###############################################################################

class LogbookProgressGraph(ProgressGraph):
    
    class EmptyLogbook(Exception):
        pass
    
    # fields that are their own unit
    INT_TITLES = ('day_l', 'night_l', 'app')
    
    DATE_FORMAT = "F jS, Y"
    
    def __init__(self, columns, *args, **kwargs):
        super(LogbookProgressGraph, self).__init__(*args, **kwargs)
        #####
        
        self.user = kwargs.pop('user') if 'user' in kwargs else None
        self.spikes = kwargs.pop('spikes') if 'spikes' in kwargs else None
        
        # split up columns and remove duplicates
        self.columns = set(columns.split('-'))
        
        from logbook.models import Flight
        self.start_qs = Flight.objects.user(self.user)
        
        self.filter_spikes()
    
    def get_annotate_field(self, column):
        from logbook.constants import DB_FIELDS
        
        if column == 'line_dist':
            return "route__total_line_all"
        
        if column in DB_FIELDS:
            return column
        elif column.endswith('pic'):
            return 'pic'
        else:
            return 'total'
        
    def filter_spikes(self):
        """
        Filter out spikes so it makes a smooth line
        """
        
        if self.spikes:
            return
        self.start_qs = self.start_qs.exclude(total__gte=24)
    
    def figure_start_and_end(self, qs):
        """
        Get the dates that the graph starts and ends. This function is for when
        a date range is not manually passed into the class
        """
        
        self.end = qs.values('date').latest()['date']
        self.start = qs.values('date').order_by('date')[0]['date']
        self.interval_start = self.start - datetime.timedelta(days=self.r)
        self.year_range = (self.end-self.start).days / 365.0
    
    def get_plots(self):
        """
        Returns a list of plot objects, one for each column
        """
        
        plots = []
        for column in self.columns:
            data = self.get_data_for_column(column)
            plots.append(self.construct_plot(data))
        
        return plots
    
       
    def get_data_for_column(self, column=None):
        """
        Returns a list of values and dates that will be plotted
        If a date range is manually specified, we must calculate the
        totals up to that date so the graph doesn't start on zero.
        """
        
        from django.db.models import Sum
        
        qs = self.start_qs.filter_by_column(column)
        db_column = self.get_annotate_field(column)
        
        if qs.count() < 1:
            raise self.EmptyLogbook
            
        before_graph = None
        if not (self.start and self.end):
            # start and end have not been passed in manually
            self.figure_start_and_end(qs)
        else:
            before_graph = qs.filter(date__lt=self.interval_start)\
                             .agg(column, float=True)
            qs = qs.filter(date__range=(self.interval_start,self.end))
        
        
        qs = qs.values('date')\
               .annotate(value=Sum(db_column))\
               .order_by('date')

        data = list(qs)
        
        
        
        if before_graph:
            # add the before graph value to the beginning of the interval data
            data.insert(0, {"date": self.interval_start-datetime.timedelta(days=1), 
                            "value": before_graph})

        return data


    def construct_plot(self, data):
        """
        Transform the raw data into plot ready lists and then construct a
        plot object
        """
        
        from utils import datetimeRange
        import numpy
        
        values = []
        dates = []
        d={}
        for item in data:
            values.append(item['value'])
            dates.append(item['date'])
            d.update({item['date']: item['value']})
            
        accumulation = numpy.cumsum(values)
        
        padx, pady = (None, ) * 2
        if self.rate:
            padx = list(datetimeRange(self.interval_start, self.end))
            pady = [d.get(day, 0) for day in padx]
            
        plot = Plot(dates, accumulation, padx=padx, pady=pady, rate=self.rate, color='b')
        return plot
    
    def output(self):
        
        ret = super(LogbookProgressGraph, self).output()
        
        from django.utils.dateformat import format
        s = format(self.start, self.DATE_FORMAT)
        e = format(self.end, self.DATE_FORMAT)
        
        subtitle = "From {0} to {1}".format(s, e)
        title = "{0} Progression".format(FIELD_TITLES[list(self.columns)[0]])
        
        self.set_titles(title, subtitle)
        
        return ret

###############################################################################
        
class Plot(object):
    
    interval = 30
    
    def __init__(self, x, y, padx=None, pady=None, **kwargs):
        self.x = x
        self.y = y
        
        assert len(x) == len(y), "%s %s" % (len(x), len(y))

        self.kwargs = kwargs
        self.kwargs['drawstyle'] = 'steps-post'
        self.kwargs['lw'] = 2
        
        self.unit = "Accumulated Flight Hours"
        self.rate_unit = "30 Day Moving Average"
        
        # must remove all kwargs that matplotlib won't accept
        
        self.do_rate = False
        if self.kwargs.pop('rate', False) and padx:
            self.do_rate = True
            self.rx = padx
            self.ry = self.moving_average(pady, self.interval)
            
    def moving_average(self, iterable, n=5):
        """
        Calculate the moving average with a subclassed deque
        http://en.wikipedia.org/wiki/Moving_average
        """
        
        from collections import deque
        d = deque([], n)
        
        avg = []
        for elem in iterable:
            d.append(elem)
            avg.append(sum(d))
            
        return avg
    
    @property
    def rate_kwargs(self):
        """
        Return keyword arguments directly into ax.plot() for the rate
        plot
        """
        
        kwargs = self.kwargs
        kwargs['lw'] = 1
        kwargs['color'] = '#c14242'
        kwargs['drawstyle'] = 'default'
        
        return kwargs
