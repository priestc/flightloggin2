from annoying.decorators import render_to
from django.contrib.auth.models import User
from django.db.models import Avg, Max, Min, Count, Sum
from logbook.models import Flight
from route.models import RouteBase
from plane.models import Plane

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
    
    most_common_tailnumber = Plane.objects\
                            .exclude(flight=None)\
                            .exclude(tailnumber='')\
                            .values('tailnumber')\
                            .distinct()\
                            .annotate(c=Count('id'))\
                            .order_by('-c')[0]['tailnumber']
                                  
    most_common_type = Plane.objects\
                            .exclude(flight=None)\
                            .exclude(type='')\
                            .values('type')\
                            .distinct()\
                            .annotate(c=Count('id'))\
                            .order_by('-c')[0]['type']
                                  
    most_common_manufacturer = Plane.objects\
                            .exclude(flight=None)\
                            .exclude(manufacturer='')\
                            .values('manufacturer')\
                            .distinct()\
                            .annotate(c=Count('id'))\
                            .order_by('-c')[0]['manufacturer']
    
    return locals()
