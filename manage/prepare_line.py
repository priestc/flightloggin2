from constants import CSV_FIELDS

class PrepareLine(object):
    """
    In comes a dict straight from the CSV file, out comes a dict formatted
    so it fits right in with the import form.
    """
    
    def __init__(self, line):
        self.line = line
        self.get_values()
    
    def output(self):
        return self.do_correct_fixing()
    
    def do_correct_fixing(self):
        """
        Determines what kind of entry this line is based on the special
        tag at the begining of each line. Assumes the first line is the
        date field.
        """      
        # if non-flight column is not empty, then this is a non-flight line
        if self.non_flying:
            return NonFlightFixer(self.line).output()
         
        elif self.date == "##RECORDS":
            return RecordsFixer(self.line).output()
           
        elif self.date == "##PLANE":
            return PlaneFixer(self.line).output()
        
        elif self.date == "##EVENT":
            return EventFixer(self.line).output()
        
        elif self.date == "##LOC":
            return LocationFixer(self.line).output()
        
        else:
            return FlightFixer(self.line).output()
        
    def get_values(self):
        """
        sets object instance variables corresponding to each valid CSV field
        """
        
        for val in CSV_FIELDS:
            setattr(self, val, self.line.get(val, ""))

###############################################################################

def fix_remarks(remarks):
    r"""
    in flightloggin 1.0, newlines are coded
    into '\r', so code the newlines back, also get rid of any invalid unicode
    characters
    """
    
    if remarks:   
        remarks = remarks.replace('\\r', '\n')
        remarks = remarks.decode("utf-8", "ignore")
        return remarks

    return ""

def combine_person(person, instructor, captain, student, fa, fo):
    """
    Turn instructor, student, etc, fields into a single person field
    """
    
    if person:
        # if person is already set, then just return that
        return person
    
    to_join=[]
    for x in [instructor, fo, captain, student, fa]:
        if x and not x == "":
            to_join.append(x)
            
    new_person=", ".join(to_join)
    
    return new_person or ""


###############################################################################     

class Fixer(object):
    def __init__(self, line):
        self.line = line
        
    def proper_mapper(self, real_column):
        """
        The special CSV lines do not have proper headers, so this function
        is used to get the proper field without needing to figure out which
        header the field falls under. This function is only needed with Events,
        Loc, Plane and all those sections. Flights do not need this because
        flight lines always have proper headers.
        """
        
        mapper = getattr(self, "mapper", False)
        
        if mapper and real_column in mapper.keys():
            return self.line.get(self.mapper[real_column])
        else:
            return self.line.get(real_column, "")
        
    def processor(self, column):
        """
        Calls the proper processor function if it exists
        processor functions are used instead of proper_mapper to return
        values that differ than whats exactly in the CSV file
        """
        proccess_function = getattr(self, column + "_processor", None)
        
        if proccess_function and callable(proccess_function):
            return proccess_function()
        else:
            raise NotImplementedError("No processor for this field")
    
    def output(self):
        ## subclass name with the "Fixer" postfix removed and made lowercase
        line_type = self.__class__.__name__[:-5].lower()
        return line_type, self.as_dict()
            
        
###############################################################################

class LocationFixer(Fixer):
    """
    In comes a line straight from the dict (with incorrect headers),
    out comes a properly formatted dict for creation of a Location object
    """
    
    mapper = {
                'identifier': 'tailnumber',
                'name': 'type',
                'lat': 'route',
                'lng': 'total',
                'municipality': 'pic',
                'loc_type': 'solo',
             }
             
    def location_processor(self):
        """
        Grabs the lattitude and longitude from the line and cats them together
        to output a WKT representation for inputting to the PointField
        """
        
        lat = self.proper_mapper('lat')
        lng = self.proper_mapper('lng')
        
        return "POINT (%s %s)" % (lat, lng)
        
        
    def as_dict(self):
        return {
                    'name':          self.proper_mapper('name'),
                    'location':      self.processor("location"),
                    'municipality':  self.proper_mapper("municipality"),
                    "loc_type":      self.proper_mapper("loc_type"),
               }
    
###############################################################################

class RecordsFixer(Fixer):

    mapper = {'records': 'tailnumber'}
    
    def records_processor(self):
    
        records = self.proper_mapper('records')
        
        if records:
            return records.replace('\\r', '\n')
        else:
            return ""   
    
    def as_dict(self):
      
        return {
                    "records": self.processor('records'),
               }

    
###############################################################################    
    
class PlaneFixer(Fixer):

    mapper = {
                'SKIP': 'date',
                'tailnumber': 'tailnumber',
                'manufacturer': 'type',
                'model': 'route',
                'type': 'total',
                'cat_class': 'pic',
                'RT': 'solo',
                'tags': 'sic',
            }
        
    def tags_processor(self):
        tags = self.proper_mapper('tags')
        rt = self.proper_mapper('RT')
        
        # add the RT column if it's there (from flightloggin 1.0)
        
        if "R" in rt and "TYPE RATING" not in tags.upper():
            tags += ', Type Rating'
            
        if "T" in rt and "TAILWHEEL" not in tags.upper():
            tags += ', Tailwheel'
        
        return tags
    
    def as_dict(self):
        return {
                    "tailnumber":   self.proper_mapper('tailnumber'),
                    "manufacturer": self.proper_mapper('manufacturer'),
                    "model":        self.proper_mapper('model'),
                    "type":         self.proper_mapper('type'),
                    "cat_class":    self.proper_mapper('cat_class'),
                    "tags":         self.processor('tags'),
                    "description":  self.proper_mapper('description'),
                }

###############################################################################

class EventFixer(Fixer):
        
    mapper = {
                  'date': 'tailnumber',
                  'non_flying': 'type',
                  'remarks': 'route',
             }
             
    def remarks_processor(self):
        return fix_remarks(self.proper_mapper('remarks')),
    
    def as_dict(self):                 
        return {
                    "date":       self.proper_mapper('date'),
                    "remarks":    self.processor('remarks'),
                    "non_flying": self.proper_mapper('non_flying'),
               }

###############################################################################

class NonFlightFixer(Fixer):
    """
    Fixes the old 'NonFlight' entries from flightloggin 1.0, which
    was mixed in with the flight section of the backup file, therefore
    no special mapping is needed
    """
    
    def non_flying_processor(self):
        from constants import NON_FLIGHT_TRANSLATE_NUM
        return NON_FLIGHT_TRANSLATE_NUM[self.proper_mapper('non_flying')]
    
    def remarks_processor(self):
        return fix_remarks(self.proper_mapper('remarks'))
    
    def as_dict(self):
        return {
                    "date":       self.proper_mapper('date'),
                    "remarks":    self.processor('remarks'),
                    "non_flying": self.processor('non_flying'),
               }
               
###############################################################################
    
class FlightFixer(Fixer):
    
    def person_processor(self):
        args = (
                self.proper_mapper('person'),
                self.proper_mapper('instructor'),
                self.proper_mapper('captain'),
                self.proper_mapper('student'),
                self.proper_mapper('fa'),
                self.proper_mapper('fo')
               )

        return combine_person(*args)
    
    def remarks_processor(self):
        return fix_remarks( self.proper_mapper('remarks') )
        
    def pilot_checkride_processor(self):
        if "P" in self.proper_mapper('flying'): return True
        return False
    
    def cfi_checkride_processor(self):
        if "C" in self.proper_mapper('flying'): return True
        return False
    
    def ipc_processor(self):
        if "I" in self.proper_mapper('flying'): return True
        return False
    
    def flight_review_processor(self):
        if "P" in self.proper_mapper('flying'): return True
        return False
    
    def tracking_processor(self):
        if "T" in self.proper_mapper('flying'): return True
        return False
    
    def holding_processor(self):
        if "H" in self.proper_mapper('flying'): return True
        return False

    def route_processor(self):
        
        route = self.proper_mapper('route')
        to =    self.proper_mapper('to')
        from_ = self.proper_mapper('from_')
        via =   self.proper_mapper('via')
        
        
        #return just the route field, if it's there
        if route:
            return route
         
        #put together "from-to" fields, then return it
        elif to and from_ and not via:
            return "%s %s" % (from_, to)
        
        #put together "from-via-to" fields, then return it
        elif to and from_ and via:
            return "%s %s %s" % (from_, via, to)
        
        # no route
        else:
            return ""
        
    def total_processor(self):
        sim = self.proper_mapper('sim')
        total = self.proper_mapper('total') 
        
        if sim and not total:
            return sim
        else:
            return total
    
    
    def as_dict(self):
    
        return {
                    "date":            self.proper_mapper('date'),
                    "tailnumber":      self.proper_mapper('tailnumber'),
                    "type":            self.proper_mapper('type'),
                    "route":           self.processor('route'),
                    
                    "total":           self.processor('total'),
                    "sim":             self.proper_mapper('sim'),
                    "pic":             self.proper_mapper('pic'),
                    "sic":             self.proper_mapper('sic'),
                    "solo":            self.proper_mapper('solo'),
                    "dual_r":          self.proper_mapper('dual_r'),
                    "dual_g":          self.proper_mapper('dual_g'),
                    "act_inst":        self.proper_mapper('act_inst'),
                    "sim_inst":        self.proper_mapper('sim_inst'),
                    "night":           self.proper_mapper('night'),
                    "xc":              self.proper_mapper('xc'),
                    
                    "app":             self.proper_mapper('app'),
                    "day_l":           self.proper_mapper('night_l'),
                    "night_l":         self.proper_mapper('day_l'),
                    
                    "remarks":         self.processor('remarks'),
                    "person":          self.processor('person'),
                    
                    "holding":         self.processor('holding'),
                    "tracking":        self.processor('tracking'),
                    
                    "pilot_checkride": self.processor("pilot_checkride"),
                    "cfi_checkride":   self.processor("cfi_checkride"),
                    "ipc":             self.processor("ipc"),
                    "flight_review":   self.processor("flight_review"),
               }
    






