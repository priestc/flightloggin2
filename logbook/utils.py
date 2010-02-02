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
    
def handle_fuel_burn(val, time):
    
    import re
    from django.forms.util import ValidationError
    
    val = val.lower()
    
    ## the value with just the number part, the unit is removed
    ## strip out all non-numeric characters but keep decimal point
    num = re.sub(r'[^\.\d\s]', '', val)
    unit = re.sub(r'[\.\d\s]', '', val)
    try:
        num = float(num)
    except:
        raise ValidationError("Invalid Fuel Burn Value")
    
    #print num, unit
    
    ####################### user entered pounds LL/pounds JetA per hour
    
    if unit == 'pphll':
        gph = num / 6
        g = gph * time
        
    elif unit == 'pphj' or unit == 'pph':
        gph = num / 6.8
        g = gph * time
        
    ####################### user entered pounds LL/pounds JetA
    
    elif unit == 'pll':
        g = num * 6
        gph = g / time
        
        
    elif unit == 'p' or unit == 'pj':
        g = num * 6.8
        gph = g / time
                
    ######################## user entered gallons or liters
    
    elif unit == 'g':
        print "g"
        g = num
        gph = (g / time)
    
    elif unit == 'l':
        print "l"
        g = num / 3.78541178 ## 1 gal = 3.78 liters
        gph = (g / time)
        
    ####################### user entered gallons/liters per hour
        
    elif unit == 'lph':
        gph = num / 3.78541178
        g = gph * time
        
    elif unit == 'gph' or unit == '':
        g = num * time
        gph = num
    
    else:
        raise ValidationError("Invalid Fuel Burn Unit")
          
    return g, gph
        
