from collections import deque

from graphs.linegraph import ProgressGraph, Plot
from models import StatDB
from constants import STATS_TITLES
from django.db.models import Max

class StatsGraph(ProgressGraph):

    def output(self):
        ret = super(StatsGraph, self).output()
        title = STATS_TITLES[self.title][0]       
        self.set_title(title)
        return ret

class SiteStatsPlot(Plot):
    
    def __init__(self, val, rate=False, **kwargs):

        self.val = str(val)

        super(SiteStatsPlot, self).__init__(rate=rate, **kwargs)
    
    def get_data(self):
        val = self.val
        
        kwarg = {val: 0}
        qs = StatDB.objects.exclude(**kwarg).order_by('dt') 
                                    
        if val.endswith("_7_days"):
            ## filter queryset to only show one data point per day
            ## this is because the 7 days graphs data is only precise to the
            ## day. Below the queryset is limited to only items that are
            ## taken at the 9 PM data poll.
            qs = qs.extra(where=['EXTRACT (HOUR FROM dt) = 18'])
        
        qs = qs.annotate(date=Max('dt'), value=Max(val))\
               .values('date', 'value')
        
        data = list(qs)
 
        self.start = data[0]['date']
        self.end = data[-1]['date']
        
        self.interval_start = self.start # no need to use a pre-interval
        
        return data
    
    def _moving_value(self, iterable):
        """
        Calculate the moving total with a deque
        slightly modified because we're calculating already-summed data
        """
        
        d = deque([], self.interval)
        
        data = []
        for elem in iterable:
            d.append(elem)
            data.append((abs(sum(d)-elem*len(d)) / len(d)) * self.interval)
            
        return data
