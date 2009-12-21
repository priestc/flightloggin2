import zipfile, StringIO

from django.http import HttpResponse
from django.template.loader import get_template
from django.template import Context

from logbook.models import Flight
from route.models import RouteBase, Route
from share.decorator import no_share

def single_route_kml(request, pk, earth):
    return HttpResponse('hi')


@no_share('other')
def airports_kml(request, shared, display_user, type_):
    from django.conf import settings
    from utils import AirportFolder 
    from airport.models import Location
    
    if type_=="all":
        title = "All Airports"
        points = Location.objects\
                         .user(display_user)\
                         .filter(loc_class=1)\
                         .distinct()
                         
        custom = Location.objects\
                         .user(display_user)\
                         .filter(loc_class=3)\
                         .distinct()
                    
        folders = []
        if points:
            folders.append(AirportFolder(name="All Airports", qs=points))
            
        if custom:
            folders.append(AirportFolder(name="All Places", qs=custom))
    
    kml = get_template('base.kml').render(
                Context({"point_folders": folders, "title": title} )
          ).encode('utf-8')
    
    ####################################
    
    sio = StringIO.StringIO()
    
    icon = settings.MEDIA_ROOT + "/icons/big/white_pad.png"
    
    z = zipfile.ZipFile(sio,'w', compression=zipfile.ZIP_DEFLATED)
    z.writestr("doc.kml", kml)
    z.write(icon, "files/icon.png")
    z.close()

    response = HttpResponse(sio.getvalue(),
                            mimetype="application/vnd.google-earth.kmz",
               )
               
    return response
    
@no_share('other')   
def routes_kml(request, shared, display_user, type_):
    from utils import RouteFolder

    if type_== "all":
        title = "All Routes"
        all_r = Route.objects.user(display_user)\
                             .values('kml_rendered', 'simple_rendered')\
                             .order_by()\
                             .distinct()

        folders=[]
        if all_r:
            folders.append(RouteFolder(name="All Routes", qs=all_r))
        
    elif type_== "cat_class":
        title = "Routes by Multi/Single Engine"
        
        single = Route.objects.user(display_user)\
                              .filter(flight__plane__cat_class__in=[1,3])\
                              .values('kml_rendered', 'simple_rendered')\
                              .order_by()\
                              .distinct()
                              
        multi = Route.objects.user(display_user)\
                             .filter(flight__plane__cat_class__in=[2,4])\
                             .values('kml_rendered', 'simple_rendered')\
                             .order_by()\
                             .distinct()
                             
        other = Route.objects.user(display_user)\
                             .exclude(flight__plane__cat_class__lte=4)\
                             .exclude(flight__plane__cat_class__gte=15)\
                             .values('kml_rendered', 'simple_rendered')\
                             .order_by()\
                             .distinct()
        
        folders = []
        if single:
            folders.append(
                RouteFolder(name="Single-Engine", qs=single, style="#red_line")
            )
            
        if multi:
            folders.append(
                RouteFolder(name="Multi-Engine", qs=multi, style="#blue_line")
            )
        
        if other:
            folders.append(
                RouteFolder(name="Other", qs=other, style="#green_line")
            )
            
    elif type_ == "flight_time":
        title = "Routes by type of flight time"
        dual_g = Route.objects.user(display_user)\
                              .filter(flight__dual_g__gt=0)\
                              .values('kml_rendered', 'simple_rendered')\
                              .order_by()\
                              .distinct()
                              
        dual_r = Route.objects.user(display_user)\
                              .filter(flight__dual_r__gt=0)\
                              .values('kml_rendered', 'simple_rendered')\
                              .order_by()\
                              .distinct()
                              
        solo =   Route.objects.user(display_user)\
                              .filter(flight__solo__gt=0)\
                              .values('kml_rendered', 'simple_rendered')\
                              .order_by()\
                              .distinct()
                              
        sic =    Route.objects.user(display_user)\
                              .filter(flight__sic__gt=0)\
                              .values('kml_rendered', 'simple_rendered')\
                              .order_by()\
                              .distinct()
                              
        inst =   Route.objects.user(display_user)\
                              .filter(flight__act_inst__gt=0)\
                              .values('kml_rendered', 'simple_rendered')\
                              .order_by()\
                              .distinct()
                              
        pic =    Route.objects.user(display_user)\
                              .filter(flight__pic__gt=0,
                                      flight__dual_g=0,
                                      flight__solo=0)\
                              .values('kml_rendered', 'simple_rendered')\
                              .order_by()\
                              .distinct()
        
        folders = []
        if dual_g:
            folders.append(
                RouteFolder(name="Dual Given", qs=dual_g, style="#orange_line")
            )
            
        if solo:
            folders.append(
                RouteFolder(name="Solo", qs=solo, style="#red_line")
            )
            
        if pic:
            folders.append(
                RouteFolder(name="PIC", qs=pic, style="#red_line")
            )
            
        if dual_r:
            folders.append(
                RouteFolder(name="Dual Received", qs=dual_r, style="#blue_line")
            )

        if sic:
            folders.append(
                RouteFolder(name="SIC", qs=sic, style="#purple_line")
            )

        if inst:
            folders.append(
                RouteFolder(name="Actual Instrument", qs=inst, style="#green_line")
            )
                
    kml = get_template('base.kml').render(
        Context({"route_folders": folders, "title": title})         
    )
    
    kml = kml.encode('utf-8')
    
    ###############################################
    
    response = HttpResponse(mimetype="application/vnd.google-earth.kmz")
    
    z = zipfile.ZipFile(response,'w', compression=zipfile.ZIP_DEFLATED)
    z.writestr("doc.kml", kml)
    
    return response
