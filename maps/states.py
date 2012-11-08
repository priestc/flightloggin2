from django.db.models import Count
from airport.models import Region, Location

def get_states_data(user, by):
    """
    Get the list of states that need to be lit up, based on the 
    """
    if by == 'unique':
        all_points = Location.objects\
                             .user(user)\
                             .filter(country="US")\
                             .distinct()

        return Region.objects\
                     .filter(location__in=all_points)\
                     .values('name')\
                     .annotate(c=Count('location__region'))

    elif by == 'relative':
        overall_data = Region.objects\
                             .filter(country='US')\
                             .values('code')\
                             .annotate(c=Count('location'))\
                             .values('c','code')

        qs = Region.objects\
                   .user(user)\
                   .filter(country='US')\
                   .values('name')\
                   .distinct()\
                   .annotate(c=Count('code')) 

        ret = {}
        for key,q in qs.items():
            ret.update({key: overall_totals[key] / q[key]})
            
        return ret

    elif by == 'count':
        return Region.objects\
                     .user(user)\
                     .filter(country='US')\
                     .values('name')\
                     .distinct()\
                     .annotate(c=Count('code'))



   
