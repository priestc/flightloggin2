from annoying.decorators import render_to
from django.contrib.auth.models import User
from django.db.models import Avg, Max, Min, Count, Sum
from logbook.models import Flight
from route.models import RouteBase

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
    unique_airports = RouteBase.objects.values('location').distinct().count()
    
    return locals()
