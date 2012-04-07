from django.db import models
from django.conf import settings

from flightloggin.logbook.fuel_burn import FuelBurn
from flightloggin.logbook.utils import expire_all, expire_logbook_cache_page
    
from flightloggin.profile.models import Profile
from flightloggin.airport.models import Location
from flightloggin.plane.models import Plane
from flightloggin.backup.models import edit_logbook
from flightloggin.logbook.models import Flight
from flightloggin.route.models import Route

def calculate_flight(sender, **kwargs):
    """
    Fill in the speed columns, and run the recalc fuel function
    """
    
    flight = kwargs['instance']
    
    if not flight.route_is_rendered():
        flight.render_route()
    
    route = flight.route
    
    #####
    
    time = flight.total    
    distance = route.total_line_all

    if distance > 0 and time > 0:  ## avoid zero division
        speed = distance / time
        flight.speed = speed
    else:
        speed = None
        
    flight.calc_fuel()
    
###############################################################################
    
def recalculate_fuel(sender, **kwargs):
    """
    When a plane is saved, all flights in that plane need to be recalculated
    to reflect the potentially updated fuelburn value
    """
    
    plane = kwargs['instance']
    
    if not plane.fuel_burn:
        return
    
    for f in Flight.objects.filter(plane=plane).iterator():
        f.calc_fuel()
        f.save()

###############################################################################

def expire_logbook_cache(sender, **kwargs):
    """
    When the user save new preferences, expire the caches on all logbook
    pages. This function is called two was: one was is by the Profile
    save signal, where sender will be the profile class, and the other way
    is by the edit_logbook signasl, in which the user instance will be the
    sender
    """
    
    page = kwargs.get('page', None)
    
    if page:
        user = sender
        expire_logbook_cache_page(user, page)
        
    elif getattr(sender, "__name__", "ff") == "Profile":
        profile = kwargs.pop('instance')
        expire_all(profile=profile)

    else:
        user = sender
        expire_all(user=user)
        
###############################################################################

def re_render_routes(sender, **kwargs):
    """
    When the user edits their locations, re-render all custom/unknown routes
    """
    
    instance = kwargs.get('instance', None)
    
    if not instance or instance.user.id == settings.COMMON_USER_ID:
        #disable this functionality when doing a location database update
        return

    qs = Route.objects\
              .user(instance.user)\
              .filter( models.Q(routebase__location__loc_class=3) | 
                       models.Q(routebase__unknown__isnull=False) |
                       models.Q(fallback_string__contains='!')
                     )\
              .distinct()

    for r in qs.iterator():
        r.hard_render()
    
###############################################################################

models.signals.post_save.connect(re_render_routes, sender=Location)
models.signals.post_delete.connect(re_render_routes, sender=Location)

models.signals.pre_save.connect(calculate_flight, sender=Flight)
models.signals.post_save.connect(recalculate_fuel, sender=Plane)    

models.signals.pre_save.connect(expire_logbook_cache, sender=Plane)
models.signals.post_save.connect(expire_logbook_cache, sender=Profile)
edit_logbook.connect(expire_logbook_cache)
