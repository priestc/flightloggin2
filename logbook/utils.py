def to_minutes(flt):
    """converts decimal to HH:MM
    
    >>> to_minutes(.5452)
    '0:33'
    >>> to_minutes(2)
    2:00
    >>> to_minutes(1.2)
    '1:12'
    >>> to_minutes(-1.2)
    '-1:12'
    """
    
    value = str(flt + 0.0)
    h,d = value.split(".")
    minutes = float("0." + d) * 60
    return str(h) + ":" + "%02.f" % minutes
    
def from_minutes(value):
    """converts HH:MM to decimal
    
    >>> from_minutes("1:45")
    1.75
    >>> from_minutes("1:75")
    2.25
    >>> from_minutes("0:17")
    0.28333333333333333
    >>> from_minutes("-4:00")
    -4.0
    """
    
    hh,mm = value.split(":")
    mm = float(mm)
    hh = float(hh)
    return (mm / 60) + hh

def proper_format(val, field, format):
    """
    Returns the value formatted appropriately based on whether it needs
    a decimal, needs to be HH:MM or needs to be an integer
    """
    
    if field in ('day_l', 'night_l', 'app'):
        #always an int; never a decimal, never hh:mm
        return str(int(val))
    
    if field in ('line_dist', 'max_width', 'gallons'):
        # always a decimal, never hh:mm
        return "%.1f" % val
            
    if format == 'decimal':
        return "%.1f" % val
    
    if format == 'minutes':
        return to_minutes(val)

def logbook_url(user, page):
    """
    Redirect the user to their logbook page, if the page==0, just redirect
    them to plain ol' logbook.html
    """
    from django.core.urlresolvers import reverse
    
    if int(page) == 0 or not page:
        kwargs = {'username': user.username}
        view = "logbook"
    else:
        kwargs = {'username': user.username, 'page': page}
        view = "logbook-page"

    return reverse(view, kwargs=kwargs)

def proper_plane_widget(profile):
    """
    Prepares the popup flight form based on how the user wants each field
    widget to be rendered as.
    """
    
    from logbook.forms import PlaneTextInput
    
    if profile.text_plane:
        return PlaneTextInput()

def expire_logbook_cache_totals(user=None):

    from django.core.cache import cache
    from django.utils.hashcompat import md5_constructor
    from django.utils.http import urlquote

    fragment_name = 'logbook_totals'
    variables = [user,]
    
    args = md5_constructor(u':'.join([urlquote(var) for var in variables]))
    cache_key = 'template.cache.%s.%s' % (fragment_name, args.hexdigest())
    cache.delete(cache_key)
    


def expire_logbook_cache_page(user=None, page=None):

    from django.core.cache import cache
    from django.utils.hashcompat import md5_constructor
    from django.utils.http import urlquote

    fragment_name = 'logbook'
    variables = [page, user]
    
    args = md5_constructor(u':'.join([urlquote(var) for var in variables]))
    cache_key = 'template.cache.%s.%s' % (fragment_name, args.hexdigest())
    cache.delete(cache_key)
    
    expire_logbook_cache_totals(user)
    

        
def expire_all(user=None, profile=None):
    """
    Expire all logbook pages in the passed user's logbook section
    This function is used after the user changes his preferences and it
    effects all pages in his logbook
    """
    
    from logbook.models import Flight
    import math
    
    if user:
        try:
            per_page = user.get_profile().per_page
        except:
            return
    
    elif profile:
        per_page = profile.per_page
        user = profile.user
    
    total_flights = Flight.objects.user(user).count()
    last_page = int(math.ceil(total_flights / float(per_page)))

    for page in range(1,last_page+1):
        expire_logbook_cache_page(user, page)


