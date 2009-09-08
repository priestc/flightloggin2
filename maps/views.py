from logbook.models import Flight
from route.models import RouteBase, Route
from is_shared import is_shared

from annoying.decorators import render_to
from django.http import HttpResponse
from django.template.loader import get_template
from django.template import Context

from is_shared import is_shared

@render_to('maps.html')
def maps(request, username):
    shared, display_user = is_shared(request, username)
    return locals()

def airports_kml(request, username):
    from settings import MEDIA_URL
    shared, display_user = is_shared(request, username)
    
    points = RouteBase.objects.filter(route__flight__user=display_user)
    
    ret = []
    for point in points:
        ret.append(point.destination())
        
    bases = set(ret)
    
    kml = get_template('base.kml').render(Context(locals() ))
    return HttpResponse(kml, mimetype="application/vnd.google-earth.kml+xml")
    
    
    
def routes_kml(request, username, type):
    shared, display_user = is_shared(request, username)
    
    class RenderedRoute(object):
        
        name = ""
        kml = ""
        
        
        def __init__(self, name, kml):
            self.kml = kml
            self.name = name
  
        
    class Folder(object):
        name = ""
        rendered_routes = []
        index = 0
        style="#base_line"
        
        def __init__(self, name, qs, style=None):
            self.rendered_routes=[]
            self.name = name
            self.qs = qs
            if style:
                self.style = style
                
            self.figure_qs()
        
        def figure_qs(self):
            for route in self.qs:
                self.rendered_routes.append(RenderedRoute(name=route['simple_rendered'], kml=route['kml_rendered']))
                
        def append(self, route):
            self.rendered_routes.append(route)
            
        def __iter__(self):
            return self
        
        def next(self):
            try:
                ret = self.rendered_routes[self.index]
            except IndexError:
                raise StopIteration
                
            self.index+=1
            return ret
        
    if type=="all":
        all_r = Route.objects.filter(flight__user=display_user).values('kml_rendered', 'simple_rendered').order_by().distinct()

        folders=[]
        if all_r:
            folders.append(Folder(name="All Routes", qs=all_r))
        
    elif type=="cat_class":
        single = Route.objects.filter(flight__user=display_user, flight__plane__cat_class__in=[1,3]).values('kml_rendered', 'simple_rendered').order_by().distinct()
        multi = Route.objects.filter(flight__user=display_user, flight__plane__cat_class__in=[2,4]).values('kml_rendered', 'simple_rendered').order_by().distinct()
        other = Route.objects.filter(flight__user=display_user).\
                exclude(flight__plane__cat_class__in=[2,4,1,3]).\
                values('kml_rendered', 'simple_rendered').order_by().distinct()
        
        folders = []
        if single:
            folders.append(Folder(name="Single-Engine", qs=single, style="#single_line"))
            
        if multi:
            folders.append(Folder(name="Multi-Engine", qs=multi, style="#multi_line"))
        
        if other:
            folders.append(Folder(name="Multi-Engine", qs=multi, style="#multi_line"))
    
    
    
    
    
    
    kml = get_template('base.kml').render(Context(locals() ))
    return HttpResponse(kml, mimetype="application/vnd.google-earth.kml+xml")
