from logbook.models import Flight
from models import get_badges_classes
import time

def new_badge(badge_classes=None, users=None):
    """
    Utility function for awarding a badge when a new one is added.
    """
    
    badge_classes = get_badges_classes() if badge_classes is None else badge_classes
    total = users.count()
    
    for i, user in enumerate(users.iterator()):
        t0 = time.time()
        flight_ids = []
        for flight in user.flight_set.order_by('date').iterator():
            flight_ids.append(flight.id)
            flights_before = Flight.objects.filter(id__in=flight_ids)
            for BadgeClass in badge_classes:
                badge = BadgeClass(all_flights=flights_before, new_flight=flight)
                badge.grant_if_eligible()

        print "-- %s" % user.username
        print "-- %.2f s" % (time.time() - t0)
        print "-- %.2f%% done" %(float(i) / total * 100)