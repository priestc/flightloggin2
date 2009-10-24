import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

import datetime

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

    def __init__(self, user, columns, dates=None):
        self.user = user
        if dates:
            dates = dates.split('-')
            s = dates[0]
            e = dates[1]
            # turn "2007.5.14" to "datetime.date(2007, 5, 14)"
            self.start = datetime.date(*[int(x) for x in s.split('.')])
            self.end   = datetime.date(*[int(x) for x in e.split('.')])
        else:
            self.start, self.end = None, None
        
        # split up columns and remove duplicates
        self.columns = set(columns.split('-'))
        
        #create the figure instance
        self.fig = plt.figure()
        
        from logbook.models import Flight
        self.start_qs = Flight.objects.user(user)
        
    def output(self):
        """get the plots, and make the titles"""
        
        #add each column plot onto the graph
        for column in self.columns:
            try:
                title, subtitle, main_plot, rate_plot = \
                self.make_twin_plot(column)
                
            except self.EmptyLogbook:
                title, subtitle, main_plot, rate_plot = \
                None, None, None, None
            
            else:    
                self.add_twin_graph(main_plot, rate_plot)
                
        if not subtitle:
            plt.figtext(.5,.5,"Nothing to Show",fontsize=18,ha='center')
            
        elif len(self.columns) > 1:
            plt.figtext(.5,.94,"Flight Time Progression", fontsize=18, ha='center')
            plt.figtext(.5,.91,subtitle,fontsize=10,ha='center')
        else:
            plt.figtext(.5,.94,title, fontsize=18, ha='center')
            plt.figtext(.5,.91,subtitle,fontsize=10,ha='center')
        
        return self.fig
    
    def make_twin_plot(self, column):
        """give it a column and a date range and it will return a rate plot
           and a main plot of that column
        """
        
        # if start and end is not already set, this function will set them,
        # it returns a dict with all the user's flights
        flights = self.get_flights_for_column(column)

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
        format_line_ticks(ax, plt, self.year_range)
        
        ax.grid(True)

        # rotates and right aligns the x labels, and moves the bottom of the
        # axes up to make room for them
        #fig.autofmt_xdate()
    
    ###########################################################################
    
    def process_data(self, flights):
        """ Takes a raw dict of flights, and does all the math processes to
            them to make cumulative and rate plots
        """
        
        from utils import datetimeRange
        
        non_padded_dates=[]
        values=[]
        dic = {}
        
        # take all dates and values and combine them into a single dict
        # flights = list of 2 item dicts, each date is unique
        # dic = one big dict with lots of items
        for item in flights:
            values.append(item['value'])
            non_padded_dates.append(item['date'])
            dic.update({item['date']: item['value']})
        
        # make accumulation
        acc_values = np.cumsum(values)

        # pad with zeroes for days that have no flights logged
        padded=[dic.get(day, 0) for day in datetimeRange(self.start, self.end)]

        month_avgs=[]
        padded_dates=[]
        date = self.start
        r = self.r
        
        for i, day in enumerate(padded):
            bottom = i-r
            if bottom < 0:
                # don't allow negative indexes, this is not what we want
                bottom=0
            
            #get the average of the previous X days (usually 30)
            month_avgs.append(  sum(padded[bottom:i])  )
            date += datetime.timedelta(days=1)
            padded_dates.append(date)
        
        #all four of these are lists
        return month_avgs, padded_dates, acc_values, non_padded_dates

    ###########################################################################
    
    def get_flights_for_column(self, column):
        """ returns a dict with all values that will be plotted """
        from django.db.models import Sum
        
        if column in DB_FIELDS:
            db_column = column
        elif column.endswith('pic'):
            db_column = 'pic'
        else:
            db_column = 'total' #FIXME: needs to handle route distance fields
        
        if self.start and self.end:
            pad = datetime.timedelta(days=1)
            s = self.start
            e = self.end
            try:
                flights = self.start_qs.filter_by_column(column).\
                        filter(date__lt=e+pad,date__gt=s-pad).\
                        values('date').\
                        annotate(value=Sum(db_column)).\
                        order_by('date')
            except AttributeError:
                raise self.EmptyLogbook
                        
            ## all stuff before the graph begins
            before_graph = self.start_qs.filter(date__lt=s-pad)
            prev_total = before_graph.agg(column)
        else:
            # drawl graph from the start
            prev_total = 0
            try:
                flights = self.start_qs.filter_by_column(column).\
                        values('date').\
                        annotate(value=Sum(db_column)).\
                        order_by('date')
            except AttributeError:
                # filter_by_column() will return None of there aren't any
                # flights in the user's logbook to satist that condition
                raise self.EmptyLogbook
        
        flights=list(flights)
        if len(flights) < 1:
            raise self.EmptyLogbook

        if not (self.start and self.end):
            try:
                # try to get the start and end dates of the user's logbook
                # automatically, if this fails, the user has no flights
                # in his/her logbook
                self.end = flights[-1]['date']
                self.start = flights[0]['date']
            except IndexError:
                # If the `flights` dict is empty, the splice indexes won't
                # work.
                raise self.EmptyLogbook
        else:
            # add the start value to the begining of the dict, so the
            # graph doesn't start at 0 when there is a date splice
            # this is only needed when an 'e' and 's' are present
            flights.insert(0, {"date": s-datetime.timedelta(days=1), 
                               "value": prev_total})
    
        # subtract both dates, convert timedelta to days,
        # divide by 365 = X.XX years
        self.year_range = (self.end-self.start).days / 365.0
    
        return flights


    def plot_colors(self, method, column):
        if method == "rate":
            return '#c14242'
        else:
            return 'b'



    def as_png(self):
        return plot_png(self.output)()
    
    def as_svg(self):
        return plot_svg(self.output)()









