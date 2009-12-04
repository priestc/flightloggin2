from constants import CSV_FIELDS

class PrepareLine(object):
    """In comes a dict straight from a CSV file, out comes a dict formatted
       so it fits right in with the import form
    """
    
    def __init__(self, line):
        self.line = line
        self.get_values()
        
        self.line_type = self.determine_type()
    
    def clean_field(self, field):
        func = getattr(self, "figure_%s" % field, "")
        if callable(func):
            # there is a clean function
            return func()
        else:
            # no clean function, use what we already have
            return {field: getattr(self, field)}

    #-----------------------------
        
    def get_values(self):
        """sets variables corresponding to each valid CSV field"""
        
        for val in CSV_FIELDS:
            setattr(self, val, self.line.get(val, ""))

    #-----------------------------        
    
    def figure_remarks(self):
        """in flightloggin 1.0, newlines are coded
        into '\r', so code the newlines back"""
        
        remarks = ""
        if self.remarks:   
            remarks = self.remarks.replace('\\r', '\n')
            
        return {'remarks': remarks}

    #-----------------------------
            
    def figure_person(self):
        """Turn instructor, student, etc, fields into a single person
           field
        """
        
        if self.person:
            # if person is already set, then just return that
            return {"person": self.person} 
        
        to_join=[]
        for x in [self.instructor, self.fo, self.captain, self.student, self.fa]:
            if not x == "":
                to_join.append(x)
                
        person=", ".join(to_join)
        
        if person:
           return {"person": person}
       
        else:
           return {'person': ""}

    #-----------------------------
       
    def figure_tracking(self):
        """if tracking value is anything but "No", then count it as
           tracking. ForPilots logbooks do it this way"""
        
        if not self.tracking:
            return {'tracking': False}
        
        
        if self.tracking.upper() == "NO":
            return {'tracking': False}
        else:
            return {'tracking': True}
        
    #-----------------------------
            
    def figure_holding(self):
        """if holding value is anything but "No", then count it as
           holding. ForPilots logbooks do it this way"""
           
        if not self.holding:
            return {'holding': False}
           
        if self.holding.upper() == "NO":
            return {'holding': False}
        else:
            return {'holding': True}
        
    #-----------------------------
    
    @property    
    def is_sim(self):
        """if there is only a sim column, but not a total column, then
           its a sim flight """
       
        return self.sim and not self.total

    #-----------------------------
        
    def figure_route(self):
        
        #return just the route field, if it's there
        if self.route:
            return {"route": self.route}
         
        #put together "from-to" fields, then return it
        elif self.to and self.from_ and not self.via:
            route = "%s %s" % (self.from_, self.to)
            return {"route": route}
        
        #put together "from-via-to" fields, then return it
        elif self.to and self.from_ and self.via:
            route = "%s %s %s" % (self.from_, self.via, self.to)
            return {"route": route}
        
        # no route
        else:
            return {'route': ''}

    #-----------------------------

    def figure_flying(self):
        """Set the proper flying column variables
        """
        dic = {}
        
        if not self.flying:
            return dic
        
        if "P" in self.flying:
            dic.update({"pilot_checkride": True})
    
        if "H" in self.flying:
            dic.update({"holding": True})
            
        if "T" in self.flying:
            dic.update({"tracking": True})
            
        if "C" in self.flying:
            dic.update({"cfi_checkride": True})
            
        if "I" in self.flying:
            dic.update({"ipc": True})
    
        return dic

    #-----------------------------
    
    def figure_non_flying(self):
        """Translates old non_flying codes to the new system
        """
        
        from constants import NON_FLIGHT_TRANSLATE_NUM
        
        if not self.non_flying:
            return {}
        
        new_number = NON_FLIGHT_TRANSLATE_NUM[self.non_flying]
        return {'non_flying': new_number}
    
    #-----------------------------
    
    def figure_total(self):
        if self.is_sim:
            return {'total': self.sim}
        else:
            return {'total': self.total}
        
    def determine_type(self):
        """Determines what kind of entry this line is based on the special
           tag at the begininf of each line. Assumes the first line of the
           date field.
        """      
        # if non-flight column is not empty, then this is a non-flight line
        if self.non_flying:
            return "nonflight"
        
        #if line starts with this tag, then it's a records line   
        elif self.date == "##RECORDS":
            return "records"
           
        elif self.date == "##PLANE":
            return "plane"
        
        elif self.date == "##EVENT":
            return "event"
        
        elif self.date == "##LOC":
            return "location"
        
        else:
            return "flight"
    
    ###########################################################################
    ###########################################################################
        
    def output(self):
        """Returns the dict based on the line type, and the line type as well
        """
        # call the proper outout method depending on the line type
        return self.line_type, getattr(self, "dict_%s" % self.line_type)()
    
    def dict_nonflight(self):
        """Create the dict as if it were a nonflight
        """
        output = {}
        for field in ('date', 'remarks', 'non_flying'):
            dic = self.clean_field(field)
            output.update(dic)
            
        return output
    
    def dict_records(self):
        """Create the dict as if it were a records
        """
        if self.tailnumber:
            return {'records': self.tailnumber.replace('\\r', '\n')}
        else:
            return {'records': ''}
    
    def dict_plane(self):
        """Create the dict as if it were a plane
        """
        from constants import PLANE_HEADERS, PLANE_MAP
        output = {}
        for field in PLANE_HEADERS:
            dic = {field: getattr(self, PLANE_MAP[field])}
            output.update(dic)
            
        tags = output.get('tags') or ""
        tagsu = tags.upper()
        
        ## translate the 'RT' column (flightloggin 1.0) to the proper tags
        if "R" in (output.get('RT') or "ff") and "TYPE RATING" not in tagsu:
            tags += ', Type Rating'
            
        if "T" in (output.get('RT') or "ff") and "TAILWHEEL" not in tagsu:
            tags += ', Tailwheel'
        
        output.update({"tags": tags}) 
        
        del output['RT']
            
        return output
        
    def dict_flight(self):
        """Create the dict as if it were a flight
        """
        
        output = {}
        for field in CSV_FIELDS:
            dic = self.clean_field(field)
            output.update(dic)
        
        # we dont need these anymore, get rid of them
        del output['via']
        del output['to']
        del output['from_']
        
        return output
    
    def dict_event(self):
        output = {}
        
        output['date'] = self.tailnumber
        output['non_flying'] = self.type
        output['remarks'] = self.route
    
    def dict_location(self):
        output = {}
        
        output['date'] = self.date
        output['non_flying'] = self.tailnumber
        output['remarks'] = self.type












