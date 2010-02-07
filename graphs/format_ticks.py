import matplotlib.dates as mdates
import matplotlib.ticker as ticker

def format_line_ticks(ax, year_range):

    if year_range < 0.05:       #just a few days showing
        ax.xaxis.set_major_locator(mdates.DayLocator())
        ax.xaxis.set_minor_locator(mdates.DayLocator())

        ax.xaxis.set_major_formatter(mdates.DateFormatter('%d'))
        
        print "ft: 1; %s" % year_range
    
    elif year_range < 0.18:       #less than a month
        ax.xaxis.set_major_locator(mdates.WeekdayLocator(byweekday=1, interval=2))
        ax.xaxis.set_minor_locator(mdates.WeekdayLocator(byweekday=1))

        ax.xaxis.set_major_formatter(mdates.DateFormatter('%d %b'))
        
        print "ft: 2; %s" % year_range

    elif year_range < 0.45:       #about six months showing
        ax.xaxis.set_major_locator(mdates.MonthLocator())
        ax.xaxis.set_minor_locator(mdates.MonthLocator(bymonthday=15))

        ax.xaxis.set_major_formatter(ticker.NullFormatter())
        ax.xaxis.set_minor_formatter(mdates.DateFormatter('%b %Y'))

        for tick in ax.xaxis.get_minor_ticks():
            tick.tick1line.set_markersize(0)
            tick.tick2line.set_markersize(0)
            tick.label1.set_horizontalalignment('center')
            
        print "ft: 3; %s" % year_range
        
    elif year_range < 1.1:       #little over a year showing
        ax.xaxis.set_major_locator(mdates.MonthLocator(bymonth=3))
        ax.xaxis.set_minor_locator(mdates.MonthLocator(bymonthday=15))

        ax.xaxis.set_major_formatter(ticker.NullFormatter())
        ax.xaxis.set_minor_formatter(mdates.DateFormatter('%b %Y'))

        for tick in ax.xaxis.get_minor_ticks():
            tick.tick1line.set_markersize(0)
            tick.tick2line.set_markersize(0)
            tick.label1.set_horizontalalignment('center')
            
        print "ft: 4; %s" % year_range
    
    elif year_range < 2.2:
        ax.xaxis.set_major_locator(mdates.MonthLocator(bymonth=(1,4,7,10)))
        ax.xaxis.set_minor_locator(mdates.MonthLocator())

        ax.xaxis.set_major_formatter(mdates.DateFormatter("%b '%y"))
        ax.xaxis.set_minor_formatter(ticker.NullFormatter())
        
        print "ft: 5; %s" % year_range
        
    elif year_range < 3.0:
        ax.xaxis.set_major_locator(mdates.MonthLocator(bymonth=(1,7)))
        ax.xaxis.set_minor_locator(mdates.MonthLocator())

        ax.xaxis.set_major_formatter(mdates.DateFormatter("%b '%Y"))
        ax.xaxis.set_minor_formatter(ticker.NullFormatter())
        
        print "ft: 6; %s" % year_range

    elif year_range < 18.3:
        ax.xaxis.set_major_locator(mdates.YearLocator())
        ax.xaxis.set_minor_locator(mdates.YearLocator(month=7))

        ax.xaxis.set_major_formatter(ticker.NullFormatter())
        ax.xaxis.set_minor_formatter(mdates.DateFormatter("'%y"))

        for tick in ax.xaxis.get_minor_ticks():
            tick.tick1line.set_markersize(0)
            tick.tick2line.set_markersize(0)
            tick.label1.set_horizontalalignment('center')
        
        print "ft: 7; %s" % year_range
            
    else:
        ax.xaxis.set_major_locator(mdates.YearLocator(10))
        ax.xaxis.set_minor_locator(mdates.YearLocator(10))

        ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))
    
        print "ft: 8; %s" % year_range
