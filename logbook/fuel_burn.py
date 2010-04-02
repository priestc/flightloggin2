import re
from django.forms.util import ValidationError
        
class FuelBurn(object):
    """
    A class that handles converting various fuel burn units
    """
    
    def __init__(self, input, time=None, mileage=None):
        
        num, unit = self.split_and_validate(input)
        
        self.gallons = None
        self.gph = None
        self.mileage = mileage
        
        if time and unit and num:
            self.time = time
            self.gallons, self.gph = self.normalize_units(num, unit, time)
    
    def split_and_validate(self, value):
        """
        Make sure the fuel burn the user entered is valid; both the unit and
        the numeric part, then return them
        """
        
        if not value:
            return None, None
        
        val = value.lower()
        
        ## the value with just the number part, the unit is removed
        ## strip out all non-numeric characters but keep decimal point
        num = re.sub(r'[^\.\d\s]', '', val)
        unit = re.sub(r'[\.\d\s]', '', val)
        
        ## all valid units the user can use
        units = ('pphll', 'pphj', 'pph', 'ppl', 'p', 'pj', 'pll',
                        'g', 'l', 'lph', 'gph' )
        
        if unit not in units:
            raise ValidationError("Invalid Fuel Burn Unit")
        
        try:
            num = float(num)
        except:
            raise ValidationError("Invalid Fuel Burn Numeric Value")
        
        return num, unit
    
    ##########################################
    
    def as_unit(self, unit, for_db=False):
        """
        Convert to a specific format for outputting. If `for_db` is true,
        return a `None` instead of an empty string
        """
        
        value = None
        
        if unit == 'liters' and self.gallons:
            value = self.gallons * 3.78541178
            
        if unit == 'gallons':
            value = self.gallons
    
        if unit == 'mpg' and self.mileage and self.gallons:
            value = self.mileage / self.gallons
        
        if unit == 'gph':
            value = self.gph
            
        ######
        
        if value:
            return "{0:.2f}".format(value)
            
        elif for_db:
            return None

        else:
            return ""
    
    ###########################################   
       
    def normalize_units(self, num, unit, time):
        """
        Given a fuelburn value in any weird format, return that value
        converted to gallons and gallons per hour.
        """
        
        if unit == 'pphll':
            gph = num / 6
            g = gph * time
            
        elif unit == 'pphj' or unit == 'pph':
            gph = num / 6.8
            g = gph * time
        
        elif unit == 'pll':
            g = num / 6
            if time > 0:
                gph = (g / time)
            else:
                gph = 0
            
        elif unit == 'p' or unit == 'pj':
            g = num / 6.8
            if time > 0:
                gph = (g / time)
            else:
                gph = 0
        
        elif unit == 'g':
            g = num
            if time > 0:
                gph = (g / time)
            else:
                gph = 0
        
        elif unit == 'l':
            g = num / 3.78541178 ## 1 gal = 3.78 liters
            if time > 0:
                gph = (g / time)
            else:
                gph = 0
            
        elif unit == 'lph':
            gph = num / 3.78541178
            g = gph * time
            
        elif unit == 'gph' or unit == '':
            g = num * time
            gph = num
        
        else:
            assert False, "Invalid Fuel Burn Unit"
              
        return g, gph
