import matplotlib.dates as mdates
import matplotlib.ticker as ticker

def format_line_ticks(ax, year_range):

    # between 0 days and 18.25 days
    # each day is major ticked, no need for a minor tick
    if 0.0 < year_range < 0.05:
        #   |      |      |      |
        #      23     24     25
        ax.xaxis.set_major_locator(mdates.DayLocator())
        ax.xaxis.set_minor_locator(mdates.DayLocator())

        ax.xaxis.set_major_formatter(mdates.DateFormatter('%d'))
        
        print "ft: 1; %s" % year_range
    
    # between 18.25 days and 2.2 months
    # each week is major ticked, each day is minor ticked
    elif 0.05 < year_range < 0.18:
        #   | . . . . . . | . . . . . . |
        #   14            21            28
        ax.xaxis.set_major_locator(mdates.DayLocator(bymonthday=(7,14,21,28)))
        ax.xaxis.set_minor_locator(mdates.DayLocator())

        ax.xaxis.set_major_formatter(mdates.DateFormatter('%d'))
        
        print "ft: 2; %s" % year_range

    #between 2.2 months (65.7 days) and 5.4 months (164.25 days)
    elif 0.18 < year_range < 0.45:
        #    |                |                |                |
        #         Oct 2009         Nov 2009         Dec 2009
        ax.xaxis.set_major_locator(mdates.MonthLocator())
        ax.xaxis.set_minor_locator(mdates.MonthLocator(bymonthday=15))

        ax.xaxis.set_major_formatter(ticker.NullFormatter())
        ax.xaxis.set_minor_formatter(mdates.DateFormatter('%b %Y'))

        for tick in ax.xaxis.get_minor_ticks():
            tick.tick1line.set_markersize(0)
            tick.tick2line.set_markersize(0)
            tick.label1.set_horizontalalignment('center')
            
        print "ft: 3; %s" % year_range
        
    elif 0.45 < year_range < 0.8:
        ax.xaxis.set_major_locator(mdates.MonthLocator())
        ax.xaxis.set_minor_locator(mdates.MonthLocator(bymonthday=15))

        ax.xaxis.set_major_formatter(ticker.NullFormatter())
        ax.xaxis.set_minor_formatter(mdates.DateFormatter("%b '%y"))

        for tick in ax.xaxis.get_minor_ticks():
            tick.tick1line.set_markersize(0)
            tick.tick2line.set_markersize(0)
            tick.label1.set_horizontalalignment('center')
            
        print "ft: 4; %s" % year_range
        
    elif 0.8 < year_range < 1.1:
        ax.xaxis.set_major_locator(mdates.MonthLocator(bymonth=(1,4,7,10)))
        ax.xaxis.set_minor_locator(mdates.MonthLocator())

        ax.xaxis.set_major_formatter(mdates.DateFormatter("%b %d"))
        ax.xaxis.set_minor_formatter(ticker.NullFormatter())

        for tick in ax.xaxis.get_minor_ticks():
            tick.tick1line.set_markersize(0)
            tick.tick2line.set_markersize(0)
            tick.label1.set_horizontalalignment('center')
            
        print "ft: 5; %s" % year_range
    
    elif 1.1 < year_range < 2.2:
        ##       |   .   .   |   .   .   |   .   .   |
        ##    Oct '08     Jan '09     Apr '09     Jul '09
        ax.xaxis.set_major_locator(mdates.MonthLocator(bymonth=(1,4,7,10)))
        ax.xaxis.set_minor_locator(mdates.MonthLocator())

        ax.xaxis.set_major_formatter(mdates.DateFormatter("%b '%y"))
        ax.xaxis.set_minor_formatter(ticker.NullFormatter())
        
        print "ft: 6; %s" % year_range
        
    elif year_range < 3.0:
        ax.xaxis.set_major_locator(mdates.MonthLocator(bymonth=(1,7)))
        ax.xaxis.set_minor_locator(mdates.MonthLocator())

        ax.xaxis.set_major_formatter(mdates.DateFormatter("%b '%Y"))
        ax.xaxis.set_minor_formatter(ticker.NullFormatter())
        
        print "ft: 7; %s" % year_range

    elif year_range < 18.3:
        ax.xaxis.set_major_locator(mdates.YearLocator())
        ax.xaxis.set_minor_locator(mdates.YearLocator(month=7))

        ax.xaxis.set_major_formatter(ticker.NullFormatter())
        ax.xaxis.set_minor_formatter(mdates.DateFormatter("'%y"))

        for tick in ax.xaxis.get_minor_ticks():
            tick.tick1line.set_markersize(0)
            tick.tick2line.set_markersize(0)
            tick.label1.set_horizontalalignment('center')
        
        print "ft: 8; %s" % year_range
            
    else:
        ax.xaxis.set_major_locator(mdates.YearLocator(10))
        ax.xaxis.set_minor_locator(mdates.YearLocator(10))

        ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))
    
        print "ft: 9; %s" % year_range
