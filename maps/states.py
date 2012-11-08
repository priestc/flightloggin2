from django.db.models import Count
from airport.models import Region, Location

def get_states_data(user, by):
    """
    Get the list of states that need to be lit up.
    by='unique' -> Count is total unique airports visited in each state
    by='landings' -> Count is the total number of landings in each state
    """
    if by == 'unique':
        all_points = Location.objects\
                             .user(user)\
                             .filter(country="US")\
                             .distinct()

        ret = Region.objects\
                     .filter(location__in=all_points)\
                     .values('code')\
                     .annotate(c=Count('location__region'))


    elif by == 'landings':
        ret = Region.objects\
                     .user(user)\
                     .filter(country='US')\
                     .values('code')\
                     .distinct()\
                     .annotate(c=Count('code'))

    new = []
    # change the code value from 'US-CA' to just 'CA'
    for item in ret:
        new.append({'count': item.get('c', 0), 'code': item['code'][3:]})

    return new