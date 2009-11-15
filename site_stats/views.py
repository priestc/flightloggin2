from annoying.decorators import render_to

@render_to('site_stats.html')
def site_stats(request):
    from django.contrib.auth.models import User
    from django.db.models import Avg, Max, Min, Count, Sum
    from logbook.models import Flight
    
    total_users = User.objects.count()
    non_empty_users = User.objects\
                          .annotate(f=Count('flight'))\
                          .filter(f__gte=1)\
                          .count()
                          
    total_flight_hours = Flight.objects.aggregate(t=Sum('total'))['t']
    total_num_flights = Flight.objects.count()
    return locals()
