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
    def __init__(self, view, height=None):
        if height:
            self.height = height
        self.view = view
    
    def __call__(self, *args, **kwargs):
        fig = self.view(*args, **kwargs)
        canvas=FigureCanvas(fig)
        response=HttpResponse(content_type='image/svg+xml')
        canvas.print_svg(response)
        return response
 
 
 
 
 
##################################################################




class plot_format(object):
    """Used for the states map"""
    extension = 'xxx'
    mime = 'xxx/xxx'    
    
    def __init__(self, view):
        self.view = view
    
    def __call__(self, *args, **kwargs):
        fig = self.view(*args, **kwargs)
        response=HttpResponse(content_type=self.mime)
        fig.savefig(response,
                    format=self.extension,
                    bbox_inches="tight",
                    pad_inches=(-0.03),)
        return response
    
class plot_svg2(plot_format):
    extension = 'svg'
    mime = 'image/svg+xml'
    
class plot_png2(plot_format):    
    extension = 'png'
    mime = 'image/png'
