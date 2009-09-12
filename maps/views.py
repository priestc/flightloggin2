import zipfile

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
    from settings import MEDIA_URL, SITE_URL
    return locals()

def airports_kml(request, username, type):
    from utils import AirportFolder 
    from airport.models import *
    shared, display_user = is_shared(request, username)
    
    if type=="all":
        title = "All Airports"
        points = Airport.objects.filter(routebase__route__flight__user=display_user).distinct()
        
        folders = []
        if points:
            folders.append(AirportFolder(name="All Airports", qs=points))
    
    kml = get_template('base.kml').render(Context({"point_folders": folders, "title": title} ))
    
    kml=kml.encode('utf-8')
    #assert False
    
    ####################################
    
    response = HttpResponse(mimetype="application/vnd.google-earth.kmz")
    
    z = zipfile.ZipFile(response,'w', compression=zipfile.ZIP_DEFLATED)
    z.writestr("doc.kml", kml)
    
    return response
    
    
    
def routes_kml(request, username, type):
    shared, display_user = is_shared(request, username)
    from utils import RouteFolder 
        
    if type=="all":
        title = "All Routes"
        all_r = Route.objects.filter(flight__user=display_user).values('kml_rendered', 'simple_rendered').order_by().distinct()

        folders=[]
        if all_r:
            folders.append(RouteFolder(name="All Routes", qs=all_r))
        
    elif type=="cat_class":
        title = "Routes by Multi/Single Engine"
        single = Route.objects.filter(flight__user=display_user, flight__plane__cat_class__in=[1,3]).values('kml_rendered', 'simple_rendered').order_by().distinct()
        multi = Route.objects.filter(flight__user=display_user, flight__plane__cat_class__in=[2,4]).values('kml_rendered', 'simple_rendered').order_by().distinct()
        other = Route.objects.filter(flight__user=display_user).\
                exclude(flight__plane__cat_class__lte=4).exclude(flight__plane__cat_class__gte=15).\
                values('kml_rendered', 'simple_rendered').order_by().distinct()
        
        folders = []
        if single:
            folders.append(RouteFolder(name="Single-Engine", qs=single, style="#red_line"))
            
        if multi:
            folders.append(RouteFolder(name="Multi-Engine", qs=multi, style="#blue_line"))
        
        if other:
            folders.append(RouteFolder(name="Other", qs=multi, style="#green_line"))
            
    elif type=="flight_time":
        title = "Routes by type of flight time"
        dual_g = Route.objects.filter(flight__user=display_user, flight__dual_g__gt=0).values('kml_rendered', 'simple_rendered').order_by().distinct()
        dual_r = Route.objects.filter(flight__user=display_user, flight__dual_r__gt=0).values('kml_rendered', 'simple_rendered').order_by().distinct()
        solo =   Route.objects.filter(flight__user=display_user,   flight__solo__gt=0).values('kml_rendered', 'simple_rendered').order_by().distinct()
        sic =    Route.objects.filter(flight__user=display_user,    flight__sic__gt=0).values('kml_rendered', 'simple_rendered').order_by().distinct()
        inst =   Route.objects.filter(flight__user=display_user,flight__act_inst__gt=0).values('kml_rendered', 'simple_rendered').order_by().distinct()
        pic =    Route.objects.filter(flight__user=display_user,    flight__pic__gt=0, flight__dual_g=0, flight__solo=0).\
                    values('kml_rendered', 'simple_rendered').order_by().distinct()
        
        folders = []
        if dual_g:
            folders.append(RouteFolder(name="Dual Given", qs=dual_g, style="#orange_line"))
            
        if solo:
            folders.append(RouteFolder(name="Solo", qs=solo, style="#red_line"))
            
        if pic:
            folders.append(RouteFolder(name="PIC", qs=pic, style="#red_line"))
            
        if dual_r:
            folders.append(RouteFolder(name="Dual Received", qs=dual_r, style="#blue_line"))

        if sic:
            folders.append(RouteFolder(name="SIC", qs=sic, style="#purple_line"))

        if inst:
            folders.append(RouteFolder(name="Actual Instrument", qs=inst, style="#green_line"))
        
    kml = get_template('base.kml').render(Context({"route_folders": folders, "title": title} ))
    
    ###############################################
    
    response = HttpResponse(mimetype="application/vnd.google-earth.kmz")
    
    z = zipfile.ZipFile(response,'w', compression=zipfile.ZIP_DEFLATED)
    z.writestr("doc.kml", kml)
    
    return response









