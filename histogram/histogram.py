from django.views.decorators.cache import cache_page
import numpy as np
from matplotlib.figure import Figure

from django.conf import settings
from django.db.models import Sum
from graphs.image_formats import plot_png, plot_svg
from main.mixins import NothingHereMixin

class BaseHistogram(NothingHereMixin):
    def __init__(self, **kwargs):      
        self.kwargs = kwargs
        self.get_data()
                 
    def output(self):

        if not self.data:
            return self.NothingHereGraph
        
        fig = Figure()
        ax = fig.add_subplot(111)

        # the histogram of the data
        ax.hist(self.data, 50, facecolor='green', alpha=0.75)

        ax.set_xlabel(self.x_label)
        ax.set_ylabel(self.y_label)
        ax.set_title(self.title)
        
        ax.minorticks_on()
        ax.grid(True)
        
        return fig
    
    def as_png(self):
        return plot_png(self.output)()

#########################################################

class UserTotalsHistogram(BaseHistogram):
    def get_data(self):
        from django.contrib.auth.models import User
        
        self.data = User.objects\
                        .exclude(id=settings.DEMO_USER_ID)\
                        .values('id')\
                        .annotate(t=Sum('flight__total'))\
                        .filter(t__isnull=False)\
                        .values_list('t', flat=True)
                        
        self.x_label = 'Total Flight Hours'
        self.y_label = 'Number of Users'
        self.title = ""

class ModelSpeedHistogram(BaseHistogram):
    def get_data(self):
        from logbook.models import Flight
        
        model = self.kwargs.pop('model')
        
        self.data = Flight.objects\
                          .user('ALL')\
                          .filter(plane__model__iexact=model)\
                          .exclude(speed__isnull=True)\
                          .exclude(speed__gte=500)\
                          .exclude(speed=0)\
                          .exclude(app__gt=1)\
                          .exclude(route__total_line_all__lt=50)\
                          .values_list('speed', flat=True)
                   
        self.x_label = "Speed of flight (knots)"
        self.y_label = "Number of flights"
        self.title = "Speed of %s Flights" % model
        
class TypeSpeedHistogram(BaseHistogram):
    def get_data(self):
        from logbook.models import Flight

        type_ = self.kwargs.pop('type_')
        
        self.data = Flight.objects\
                          .user('ALL')\
                          .filter(plane__type__iexact=type_)\
                          .exclude(speed__isnull=True)\
                          .exclude(speed=0)\
                          .exclude(app__gt=1)\
                          .exclude(route__total_line_all__lt=50)\
                          .values_list('speed', flat=True)
                   
        self.x_label = "Speed of flight (knots)"
        self.y_label = "Number of flights"
        self.title = "Speed of %s Flights" % type_






