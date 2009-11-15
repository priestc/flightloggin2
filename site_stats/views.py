from annoying.decorators import render_to
from django.contrib.auth.models import User
from django.db.models import Avg, Max, Min, Count, Sum
from logbook.models import Flight
from route.models import RouteBase, Route
from plane.models import Plane
from django_openid_auth.models import UserOpenID

@render_to('site_stats.html')
def site_stats(request):
    
    total_users = User.objects.count()
    non_empty_users = User.objects\
                          .annotate(f=Count('flight'))\
                          .filter(f__gte=1)\
                          .count()
                          
    total_flight_hours = Flight.objects.aggregate(t=Sum('total'))['t']
    total_num_flights = Flight.objects.count()
    avg_per_active = total_flight_hours / non_empty_users
    avg_per_flight = total_flight_hours / total_num_flights
    unique_airports = RouteBase.objects.values('location').distinct().count()
    unique_countries = RouteBase.objects.values('location__country').distinct().count()
    
    p = Plane.objects\
            .exclude(flight=None)\
            .exclude(tailnumber='')\
            .values('tailnumber')\
            .distinct()\
            .annotate(c=Count('id'))\
            .order_by('-c')[0]
            
    most_common_tailnumber = p['tailnumber']
    most_common_tailnumber_count = p['c']
                                  
    p = Plane.objects\
            .exclude(flight=None)\
            .exclude(type='')\
            .values('type')\
            .distinct()\
            .annotate(c=Count('id'))\
            .order_by('-c')[0]
                            
    most_common_type = p['type']
    most_common_type_count = p['c']     
                             
    p = Plane.objects\
            .exclude(flight=None)\
            .exclude(manufacturer='')\
            .values('manufacturer')\
            .distinct()\
            .annotate(c=Count('id'))\
            .order_by('-c')[0]
                            
    most_common_manu = p['manufacturer']
    most_common_manu_count = p['c']
    
    total_dist = Route.objects.aggregate(s=Sum('total_line_all'))['s']
    total_dist_earth = total_dist / 21620.6641
    
    google = UserOpenID.objects.filter(claimed_id__contains='google').count()
    g_p = google / float(total_users) * 100
    
    yahoo = UserOpenID.objects.filter(claimed_id__contains='yahoo').count()
    y_p = yahoo / float(total_users) * 100
    
    my = UserOpenID.objects.filter(claimed_id__contains='myopenid').count()
    m_p = my / float(total_users) * 100
    
    aol = UserOpenID.objects.filter(claimed_id__contains='openid.aol').count()
    a_p = aol / float(total_users) * 100
    
    others = total_users - (aol + my + yahoo + google)
    o_p = others / float(total_users) * 100
    
    return locals()
