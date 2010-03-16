import datetime
import numpy
from collections import deque

from django.utils.dateformat import format
from django.db.models import Sum
        
from matplotlib.figure import Figure

from logbook.constants import FIELD_TITLES, DB_FIELDS
from logbook.models import Flight
from main.mixins import NothingHereMixin

from utils import datetimeRange
from image_formats import plot_png, plot_svg, plot_png2, plot_svg2


class EmptyGraph(Exception):
        pass

class ProgressGraph(NothingHereMixin):
    """
    Given a list of plot objects, return a Matplotlib line graph.
    """
    
    # the date format of the subtitle
    df = "F jS, Y"

    def __init__(self, plots):
        
        self.fig = Figure()
        self.plots = plots
        
        self.ax2 = None
        
        overall_range = self.overall_range(plots)
        
        if not overall_range:
            self.start, self.end, self.year_range = (None,) * 3
        else:
            self.start, self.end, self.year_range = overall_range
    
    def overall_range(self, plots):
        """
        Go through each plot object and determine the overall range
        across all of them
        """
        
        starts = []
        ends = []
        for plot in plots:
            starts.append(plot.start)
            ends.append(plot.end)
        
        overall_e = max(ends)
        overall_s = min(starts)
        overall_y = (overall_e - overall_s).days / 365.0
        
        return (overall_s, overall_e, overall_y)
    
    def set_titles(self, title, subtitle):
        """
        Set the title and subtitle of the graph
        """
        
        self.fig.text(.5,.94,title, fontsize=18, ha='center')
        self.fig.text(.5,.91,subtitle,fontsize=10,ha='center')
    
    def output(self):

        for plot in self.plots:
            self.add_plot(plot)
            
        self.fig.gca().set_xlim(self.start, self.end)
        
        return self.fig
    
    def add_plot(self, plot):
        ax = self.fig.add_subplot(111)
        ax.plot(plot.x, plot.y, **plot.kwargs)
        ax.set_ylabel(plot.unit)
        
        if plot.do_rate:
            c = plot.rate_kwargs['color']
            if not self.ax2:
                # add all rate graphs to the same axis
                self.ax2 = ax.twinx()
                
            self.ax2.plot(plot.rx, plot.ry, **plot.rate_kwargs)
            self.ax2.set_ylabel(plot.rate_unit, color=c)
            
            for tl in self.ax2.get_yticklabels():
                tl.set_color(c)
        
        from format_ticks import format_line_ticks    
        format_line_ticks(ax, self.year_range)
        ax.grid(True)
    
    @plot_png
    def as_png(self):
        try:
            return self.output()
        except EmptyGraph:
            return self.NothingHereGraph
    
    @plot_svg
    def as_svg(self):
        try:
            return self.output()
        except EmptyGraph:
            return self.NothingHereGraph

###############################################################################

class LogbookProgressGraph(ProgressGraph):
    
    # fields that are their own unit
    INT_TITLES = ('day_l', 'night_l', 'app')
    
    DATE_FORMAT = "F jS, Y"
      
    def output(self):
        
        ret = super(LogbookProgressGraph, self).output()
        
        s = format(self.start, self.DATE_FORMAT)
        e = format(self.end, self.DATE_FORMAT)
        
        subtitle = "From {0} to {1}".format(s, e)
        
        title = []
        for plot in self.plots:
            title.append(plot.title)
        
        title = "{0} Progression".format(", ".join(title))
        
        self.set_titles(title, subtitle)
        
        return ret

###############################################################################
        
class Plot(object):
    
    interval = 30
    
    def __init__(self, data, rate=False, **kwargs):
        """
        All subclasses need to first determine self.start and self.end, and
        self.title before this constructor can be called with super()
        """
        
        self.x, self.y, padx, pady = self.construct_plot_lists(data, rate)

        self.kwargs = kwargs
        self.kwargs['drawstyle'] = 'steps-post'
        self.kwargs['lw'] = 2
        
        self.unit = "Accumulated Flight Hours"
        self.rate_unit = "30 Day Moving Total"
        
        self.do_rate = False
        if rate:
            self.do_rate = True
            self.rx = padx
            self.ry = self.moving_average(pady)
            
    def moving_average(self, iterable):
        """
        Calculate the moving average with a deque
        http://en.wikipedia.org/wiki/Moving_average
        """
        
        d = deque([], self.interval)
        
        avg = []
        for elem in iterable:
            d.append(elem)
            avg.append(sum(d))
            
        return avg

    def construct_plot_lists(self, data, rate):
        """
        Transform the raw data into plot ready lists: x, y.
        And for the rate: padx, pady
        """
        
        values = []
        dates = []
        d={}
        for item in data:
            values.append(item['value'])
            dates.append(item['date'])
            d.update({item['date']: item['value']})
            
        accumulation = numpy.cumsum(values)
        
        if rate:
            padx = list(datetimeRange(self.interval_start, self.end))
            pady = [d.get(day, 0) for day in padx]
        else:
            padx = None
            pady = None
        
        return dates, accumulation, padx, pady
    
    def split_dates(self, date_range):
        """
        Split up the date in url form and return them as
        datetime objects
        """
        
        dates = date_range.split('-')
        s = dates[0]
        e = dates[1]
        
        # turn "2007.5.14" to "datetime.date(2007, 5, 14)"
        start = datetime.date(*[int(x) for x in s.split('.')])
        end   = datetime.date(*[int(x) for x in e.split('.')])
        
        return (start, end)
    
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

##############################################################################

class LogbookPlot(Plot):
    
    def __init__(self, user, column, range=None, rate=False, spikes=True, **kwargs):
        """
        Turns a username, column name and a date range into a big single
        list data from the database. self.interval_start is used internally
        to help
        """
        
        self.start_qs = Flight.objects.user(user).filter_by_column(column)
        
        self.title = FIELD_TITLES[column]
        
        if not spikes:
            self.filter_spikes()
            
        if range:
            # range is the date range of the visible plot. Here we convert
            # those dates from a string to a datetime object
            self.start, self.end = self.split_dates(range)
        else:
            # Determine the start and end of the graph based on
            # some extra database queries.
            self.start, self.end = self.figure_start_and_end(self.start_qs)
            
        self.interval_start = self.start
        if rate:
            #go back another [interval] days if we're making a rate graph
            #this is so the rate line is fully accurate when the plot starts 
            self.interval_start -= datetime.timedelta(days=self.interval)
        
        data = self.get_data(column)
            
        super(LogbookPlot, self).__init__(data, rate, **kwargs)

    def figure_start_and_end(self, qs):
        """
        Get the dates that the graph starts and ends. This function is for when
        a date range is not manually passed into the class
        """
        try:
            end = qs.values('date').latest()['date']
            start = qs.values('date').order_by('date')[0]['date']
        except Flight.DoesNotExist:
            raise EmptyGraph

        return (start, end)

    def get_annotate_field(self, column):
        """
        Returns a db field name for use in the annotate function
        """
        
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
        
        self.start_qs = self.start_qs.exclude(total__gte=24)
    
    def get_data(self, column):
        """
        Returns a list of dicts containing values and dates
        which will be sent off to more processing. This data is
        filtered to the appropriate date range.
        """
        
        qs = self.start_qs
        db_column = self.get_annotate_field(column)
        
        if qs.count() < 1:
            raise self.EmptyLogbook
            
        before_graph = qs.filter(date__lt=self.interval_start)\
                         .agg(column, float=True)
                         
        qs = qs.filter(date__range=(self.interval_start,self.end))\
               .values('date')\
               .annotate(value=Sum(db_column))\
               .order_by('date')

        data = list(qs)
        
        # add the before graph value to the beginning of the interval data
        data.insert(0, {"date": self.interval_start-datetime.timedelta(days=1), 
                        "value": before_graph})

        return data

















