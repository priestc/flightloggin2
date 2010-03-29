from django.db import models

from backup.models import edit_logbook
from logbook.models import Flight
from logbook.fuel_burn import FuelBurn
from logbook.utils import expire_all, expire_logbook_cache_page
from profile.models import Profile
from plane.models import Plane

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
        print "recalc due to plane save", f.plane.tailnumber
        f.calc_fuel()
        print "NUMERIC GALLONS", f.gallons
        f.save()
        print "NUMERIC GALLONS AGAIN", f.gallons

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

models.signals.pre_save.connect(calculate_flight, sender=Flight)
models.signals.post_save.connect(recalculate_fuel, sender=Plane)    
models.signals.post_save.connect(expire_logbook_cache, sender=Profile)
edit_logbook.connect(expire_logbook_cache)
