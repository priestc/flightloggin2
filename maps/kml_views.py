import zipfile, StringIO

from django.http import HttpResponse
from django.template.loader import get_template
from django.template import Context

from logbook.models import Flight
from route.models import RouteBase, Route
from share.decorator import no_share

from utils import RouteFolder

def single_tailnumber_kml(request, tn):
    """ Returns a KMZ of all routes flown by the passed tailnumber"""
    
    qs = Route.objects.filter(flight__plane__tailnumber=tn)
                  
    return qs_to_time_kmz(qs)

def single_route_kml(request, pk, earth):
    if not earth:
        from django.conf import settings
        from django.core.urlresolvers import reverse
        from django.http import HttpResponseRedirect
        url = reverse('s-route-kml', kwargs={"pk":pk})
        gm = "http://maps.google.com?q=%s%s" % (settings.SITE_URL, url)
        return HttpResponseRedirect(gm)
        
        
    from utils import RouteFolder
    r = Route.objects.filter(flight__pk=pk)\
                     .values('kml_rendered', 'simple_rendered')
                     
    f = RouteFolder(name="Route", qs=r, style="#red_line")

    return folders_to_kmz_response([f])

def single_location_kml(request, pk):
    qs = Route.objects.filter(routebase__location__identifier=pk.upper())               
    return qs_to_time_kmz(qs)

def qs_to_time_kmz(qs):
    """ From a routes queryset, return a folder'd up kmz file split up
        by type of flight time. pic, sic, dual received, etc
    """
    
    title = "Routes by type of flight time"
    
    dual_g = qs.filter(flight__dual_g__gt=0)\
               .values('kml_rendered', 'simple_rendered')\
               .order_by()\
               .distinct()
              
    dual_r = qs.filter(flight__dual_r__gt=0)\
               .values('kml_rendered', 'simple_rendered')\
               .order_by()\
               .distinct()
                          
    solo =   qs.filter(flight__solo__gt=0)\
               .values('kml_rendered', 'simple_rendered')\
               .order_by()\
               .distinct()
                          
    sic =    qs.filter(flight__sic__gt=0)\
               .values('kml_rendered', 'simple_rendered')\
               .order_by()\
               .distinct()
                          
    inst =   qs.filter(flight__act_inst__gt=0)\
               .values('kml_rendered', 'simple_rendered')\
               .order_by()\
               .distinct()
                          
    pic =    qs.filter(flight__pic__gt=0,
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


    return folders_to_kmz_response(folders, title)



def qs_to_catclass_kmz(qs):
    """ From a routes queryset, return a folder'd up kmz file split up
        by categoty class of the plane. single multi, helicopter, etc
    """
    
    title = "Routes by Multi/Single Engine"
        
    single = qs.filter(flight__plane__cat_class__in=[1,3])\
               .values('kml_rendered', 'simple_rendered')\
               .order_by()\
               .distinct()
                          
    multi = qs.filter(flight__plane__cat_class__in=[2,4])\
              .values('kml_rendered', 'simple_rendered')\
              .order_by()\
              .distinct()
                         
    other = qs.exclude(flight__plane__cat_class__lte=4)\
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
        
    return folders_to_kmz_response(folders, title)














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
    
    return folders_to_kmz_response(folders, title)





























 
@no_share('other')   
def routes_kml(request, shared, display_user, type_):
    
    qs = Route.objects.user(display_user)
    
    if type_== "all":
        title = "All Routes"
        all_r = qs.values('kml_rendered', 'simple_rendered')\
                  .order_by()\
                  .distinct()

        folders=[]
        if all_r:
            folders.append(RouteFolder(name="All Routes", qs=all_r))
        
        return folders_to_kmz_response(folders, title)
        
    elif type_== "cat_class":
        return qs_to_time_kmz(qs)
            
    elif type_ == "flight_time":
        return qs_to_time_kmz(qs)
                
    

def folders_to_kmz_response(folders, title=None):
    
    kml = get_template('base.kml').render(
        Context({"route_folders": folders})         
    )
    
    kml = kml.encode('utf-8')
    
    ###############################################
    
    response = HttpResponse(mimetype="application/vnd.google-earth.kmz")
    
    z = zipfile.ZipFile(response,'w', compression=zipfile.ZIP_DEFLATED)
    z.writestr("doc.kml", kml)
    
    return response
