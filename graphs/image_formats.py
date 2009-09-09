from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from django.http import HttpResponse

class plot_png(object):
    def __init__(self, view):
        self.view = view
    
    def __call__(self, *args, **kwargs):
        fig = self.view(*args, **kwargs)
        canvas=FigureCanvas(fig)
        response=HttpResponse(content_type='image/png')
        canvas.print_png(response)
        return response
        
class plot_svg(object):
    def __init__(self, view):
        self.view = view
    
    def __call__(self, *args, **kwargs):
        fig = self.view(*args, **kwargs)
        canvas=FigureCanvas(fig)
        response=HttpResponse(content_type='image/svg+xml')
        canvas.print_svg(response)
        return response