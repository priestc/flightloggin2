from django.contrib.auth.models import User
from logbook.models import Flight
import time

def new_badge(badge_classes, test=False):
    """
    Utility function for awarding a badge when a new one is added.
    """
    if test:
        users = [User.objects.get(username='chris')]
    else:
        users = User.objects.all()
    
    for user in users:
        print user.username
        t0 = time.time()
        flight_ids = []
        for flight in user.flight_set.order_by('date'):
            flight_ids.append(flight.id)
            flights_before = Flight.objects.filter(id__in=flight_ids)
            for BadgeClass in badge_classes:
                badge = BadgeClass(all_flights=flights_before, new_flight=flight)
                badge.grant_if_eligible()
        print "-- %.2f" % (time.time() - t0)