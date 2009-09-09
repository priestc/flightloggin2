class RenderedRoute(object):
    name = ""
    kml = ""
    
    def __init__(self, name, kml):
        self.kml = kml
        self.name = name
        
class RouteFolder(object):
    name = ""
    rendered_routes = []
    index = 0
    style="#red_line"

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
        
    def __iter__(self):
        return self

    def next(self):
        try:
            ret = self.rendered_routes[self.index]
        except IndexError:
            raise StopIteration
            
        self.index+=1
        return ret

#########################################################################################################################################

class RenderedAirport(object):
    name = ""
    kml = ""
    identifier = ""
    ls = ""  #location summary: fancy name for the location, e.g.: "Newark, Ohio"; "Lolongwe, Malawi"
    
    def __init__(self, destination):
        self.kml = "%s,%s,0" % (destination.location.x, destination.location.y)
        self.name = destination.name
        self.ls = destination.location_summary()
        self.identifier = destination.identifier
    
class AirportFolder(RouteFolder):
    name = ""
    rendered_airports = []
    index = 0
    style="#red_line"

    def __init__(self, name, qs, style=None):
        self.rendered_airports=[]
        self.name = name
        self.qs = qs
        if style:
            self.style = style
            
        self.figure_qs()

    def __str__(self):
        return "<AF: %s>" % len(self.rendered_airports)

    def figure_qs(self):
        for airport in self.qs:
            if airport.location:
                ra=RenderedAirport(destination=airport)
                self.rendered_airports.append(ra)

    def next(self):
        try:
            ret = self.rendered_airports[self.index]
        except IndexError:
            raise StopIteration
            
        self.index+=1
        return ret







