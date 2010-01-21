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
        return str(int(val))
    
    if field in ('line_dist', 'max_width'):
        return "%.1f" % val
            
    if format == 'decimal':
        return "%.1f" % val
    
    if format == 'minutes':
        return to_minutes(val)
