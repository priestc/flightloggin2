import datetime
import numpy as np

from django.utils.dateformat import format as dj_date_format

from image_formats import plot_png, plot_svg, plot_png2, plot_svg2
from logbook.constants import FIELD_TITLES, DB_FIELDS

class ProgressGraph(object):

    # the date format of the subtitle
    df = "F jS, Y"
    
    # the window for rate calculations
    r = 30
    
    # fields that are their own unit
    INT_TITLES = ('day_l', 'night_l', 'app')
    
    class EmptyLogbook(Exception):
        pass

    def __init__(self, user, columns, dates=None, rate=True, spikes=True):
        self.user = user
        self.rate = rate
        if dates:
            dates = dates.split('-')
            s = dates[0]
            e = dates[1]
            # turn "2007.5.14" to "datetime.date(2007, 5, 14)"
            self.start = datetime.date(*[int(x) for x in s.split('.')])
            self.end   = datetime.date(*[int(x) for x in e.split('.')])
            self.year_range = (self.end-self.start).days / 365.0
        else:
            self.start, self.end = None, None
        
        # split up columns and remove duplicates
        self.columns = set(columns.split('-'))
        
        #create the figure instance
        from matplotlib.figure import Figure
        self.fig = Figure()
        
        from logbook.models import Flight
        self.start_qs = Flight.objects.user(user)
        
        time = columns.split('-')[0]
        if not spikes:
            #filter out spikes so it makes a smooth line
            kwarg = {"%s__gte" % str(time): "24"}
            self.start_qs = self.start_qs.exclude(**kwarg)
            
        if self.rate:
            pad = datetime.timedelta(days=30)
            self.pad_start = self.start - pad
            self.pad_end = self.end + pad
    
    def output(self)
        
        for column in self.columns:
            if self.start and self.end:
                plot_tup = self.restricted_plot(column, rate=self.rate)     
            else
                plot_tup = self.unrestricted_plot(column, rate=self.rate)

    ###########################################################################
    
    def make_twin_plot(self, column):
        """give it a column and a date range and it will return a rate plot
           and a main plot of that column
        """
        
        # if start and end is not already set, this function will set them,
        # it returns a dict with all the user's flights
        flights = self.get_data(column)

        #######################
        
        # all the heavy mathematical calculating is done here
        month_avgs, padded_dates, acc_values, non_padded_dates = \
                                    self.process_data(flights)
        
        ############ format graph variables
        
        title = '%s Progession' % FIELD_TITLES[column]
        
        subtitle = "From %s to %s" % (dj_date_format(self.start, self.df),
                                      dj_date_format(self.end,   self.df))
        
        if column in self.INT_TITLES:
            # integer fields such as landings and approaches
            acc_unit = '%s' % FIELD_TITLES[column]
            rate_unit = '%s per month' % FIELD_TITLES[column]
        else:
            # flight hour fields (pretty much everything else)
            acc_unit = 'Flight Hours'
            rate_unit = 'Flight Hours per month'
            
        acc_plot={"x": non_padded_dates,
                  "y": acc_values,
                  "y_unit": acc_unit,
                  "color": self.plot_colors('main', column)}
               
        rate_plot={"x": padded_dates,
                   "y": month_avgs,
                   "y_unit": rate_unit,
                   "color": self.plot_colors('rate', column)}
        
        return (title, subtitle, acc_plot, rate_plot)
    
    
    def get_data(self, column):
        """ returns a dict with all values that will be plotted """
        
        # all flights logbook wide that are of that column
        # not restricted to any date interval (yet)
        qs = self.start_qs.filter_by_column(column)
        
        if self.start and self.end and self.rate:
            # the interval is restricted, and we want to show the rate
            # so expand by 30 days so the rate graph isn't messed up
            
            flights = qs.filter(date__lt=self.p_end,
                                date__gt=self.p_start)\
                        .order_by('date')
                        
            # the starting point of the graph, sum of all flights before
            # the interval began
            start = qs.filter(date__lte=self.start).agg(column)
            start = float(start) ## agg function always returns a string
                                    
        elif self.start and self.end:
            # the interval is restricted, but we don't want to show the rate
            # so don't bother expanding the interval
            flights = qs.filter(date__lt=self.end,
                                date__gt=self.start)\
                        .order_by('date')
            
            # the starting point of the graph, sum of all flights before
            # the interval began
            start = qs.filter(date__lte=self.start).agg(column)
            start = float(start) ## agg function always returns a string
    
        else:
            # the interval is not restricted
            flights = qs.order_by('date')
            flights = list(flights)
            
            
        
        flights = list(flights.agg_by_date(column))
        if len(flights) < 1:
            raise self.EmptyLogbook

        
        if self.start and self.end:
            day_before_start = self.start - datetime.timedelta(days=30)
            
            flights.insert(0, {"date": day_before_start, 
                               "value": start}
                          )  
    
        return flights

    def add_twin_graph(self, acc_plot, rate_plot):
        """give it a plot dict and it will return a graph image"""
       
        ax = self.fig.add_subplot(111)
        ax.plot(acc_plot['x'],
                acc_plot['y'],
                color=acc_plot['color'],
                drawstyle='steps-post', lw=2)
                
        ax.set_ylabel(acc_plot['y_unit'],
                      color=acc_plot['color'], )
        
        ax.set_xlim(self.start, self.end)
        
        if self.rate:
            #only add if the user wants the rate shown
            ax2 = ax.twinx()
            d_color='#c14242'
            ax2.plot(rate_plot['x'],
                     rate_plot['y'],
                     color=rate_plot['color'],
                     drawstyle='default')
                     
            ax2.set_ylabel(rate_plot['y_unit'],
                           color=rate_plot['color'], )
            
            for tl in ax2.get_yticklabels():
                tl.set_color(d_color)
            
        # format the ticks based on the range of the dates
        from format_ticks import format_line_ticks
        format_line_ticks(ax, self.year_range)
        
        ax.grid(True)

    def plot_colors(self, method, column):
        if method == "rate":
            return '#c14242'
        else:
            return 'b'
        
    def as_png(self):
        return plot_png(self.output)()
    
    def as_svg(self):
        return plot_svg(self.output)()
