from django.db.models import Sum
from image_formats import plot_png, plot_svg, plot_png2, plot_svg2
class Histogram(object):
    def __init__(self):
        from django.contrib.auth.models import User
        self.data = User.objects\
                        .values('id')\
                        .annotate(t=Sum('flight__total'))\
                        .filter(t__isnull=False)\
                        .values_list('t', flat=True)
                        
    def output(self):
        import numpy as np
        import matplotlib
        matplotlib.use('Agg')
        import matplotlib.pyplot as plt
        
        fig = plt.figure()
        ax = fig.add_subplot(111)

        # the histogram of the data
        ax.hist(self.data, 60, facecolor='green', alpha=0.75)

        ax.set_xlabel('Total Flight Hours')
        ax.set_ylabel('Number of Users')
        ax.minorticks_on()

        #ax.set_xlim(0, 2000)
        ax.grid(True)
        
        return fig
    
    def as_png(self):
        return plot_png(self.output)()
