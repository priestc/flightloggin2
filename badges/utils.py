from logbook.models import Flight
from models import get_badges_classes
import time

from collections import defaultdict

def new_badge(badge_classes=None, users=None):
    """
    Utility function for awarding a badge when a new badge is defined.
    """
    
    badge_classes = get_badges_classes() if badge_classes is None else badge_classes
    total = users.count()
    
    performance = defaultdict(lambda: [])
    process_start = time.time()
    overall_total_flights = Flight.objects.filter(user__in=users).count()
    total_flights_processed = 0

    for user_i, user in enumerate(users.iterator()):
        user_start = time.time()
        flight_ids = []
        flights = user.flight_set.order_by('date')
        total_flights = flights.count()
        for flight_i, flight in enumerate(flights.iterator()):
            flight_ids.append(flight.id)
            flights_before = Flight.objects.filter(id__in=flight_ids)
            flight_start = time.time()
            for BadgeClass in badge_classes:
                badge_start = time.time()
                badge = BadgeClass(all_flights=flights_before, new_flight=flight)
                badge.grant_if_eligible()
                time_for_badge = time.time() - badge_start
                
                print "%s - %.2f%% -- %.3f" % (
                    user.username,
                    (float(total_flights_processed) / overall_total_flights) * 100,
                    time.time() - badge_start
                )

            total_flights_processed += 1

    return performance