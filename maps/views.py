from logbook.models import Flight
from route.models import Route
from is_shared import is_shared

def airports_kml(request, username):
    
    shared, display_user = is_shared(request, username)
    
    routes = Routes.objects.filter(flight__user=display_user)
