import datetime
import csv

from records.forms import NonFlightForm
from logbook.models import Flight
from records.models import Records, NonFlight
from plane.models import Plane

class BaseImport(object):
    
    class NoFileError(Exception):
        pass
    
    class InvalidCSVError(Exception):
        pass
    
    def __init__(self, user, f):
        
        self.user = user
        self.f = f
            
        if not self.f:
            raise self.NoFileError
        
        self.flight_out = []
        self.plane_out = []
        self.records_out = []
        self.non_out = []
        
    def do_pre(self):
        """get the first 10,000 characters of the file for preview purposes"""
        self.f.seek(0)
        self.pre = self.f.read(10000)
        self.f.seek(0)
        
    def get_dialect(self):
        self.do_pre()
        try:
            return csv.Sniffer().sniff(self.pre)
        except:
            raise self.InvalidCSVError
        
        
    def get_dict_reader(self):
        """makes a dictreader that is seek'd to the first valid line of data"""
        
        dialect = self.get_dialect()
        if dialect.delimiter == " ":
            dialect.delimiter = "\t"
               
        try:
            reader = csv.reader(self.f, dialect)
        except TypeError:
            raise RuntimeError, "Not a valid CSV file"
        
        titles = reader.next()
        titles = self.swap_out_flight_titles(titles)
        
        self.dr = csv.DictReader(self.f, titles, dialect=dialect)
        self.dr.next()
            
    def action(self):
        """Go through each line, determine which type it is, then hand off that
           line to the proper function.
        """

        from prepare_line import PrepareLine
        
        self.get_dict_reader()
        
        for line in self.dr:
            line_type, dic = PrepareLine(line).output()
            
            if line_type == "flight":
                self.flight_out.append( self.handle_flight(dic) )

            elif line_type == "nonflight":
                self.non_out.append( self.handle_nonflight(dic) )
                
            elif line_type == "records":
                self.records_out.append( self.handle_records(dic) )
                
            elif line_type == "plane":
                self.plane_out.append( self.handle_plane(dic) )
        
        self.make_headers()
        
    def swap_out_flight_titles(self, original):
        """transform the headers of the user's CSV file to normalized headers
           which can be processed.
        """
        from constants import COLUMN_NAMES
        new = []
        for title in original:
            # replace /n and /r because of logbook pro
            title = title.upper().strip().replace("\"", '').replace(".", "").\
                    replace("\r\n", " ")
            if title in COLUMN_NAMES.keys():
                new.append(COLUMN_NAMES[title])
            else:
                new.append(title)
                
        return new
    
    def make_headers(self):
        from logbook.constants import FIELD_ABBV
        from constants import PREVIEW_FIELDS
        
        fh = ["<td>%s</td>" % FIELD_ABBV[f] for f in PREVIEW_FIELDS]
        self.flight_header = "<tr class=\"header\">" + "".join(fh) + "</tr>"
        
        ##########
        
        ph = ["<td>%s</td>" % f for f in ('Registration', 'Type', 'Manufacturer',
                                          'Model', 'Category/Class', 'Tags')]
                                          
        self.plane_header = "<tr class=\"header\">" + "".join(ph) + "</tr>"
        
        ##########
        
        nh = ["<td>%s</td>" % f for f in ('Date', 'Type', 'Remarks',)]
                                          
        self.non_flight_header = "<tr class=\"header\">" + "".join(nh) + "</tr>"

###############################################################################

class PreviewImport(BaseImport):

    def handle_flight(self, line, submit=None):
        
        out = ["<tr>"]
        from constants import PREVIEW_FIELDS
        for field in PREVIEW_FIELDS:
            out.append("<td class='%s'>%s</td>" % (field, line[field]))
            
        out.append("</tr>")
        
        # add the output of this line to the output list
        return "".join(out)

    def handle_nonflight(self, line, submit=None):
        
        date = "<td>%s</td>" % line['date']
        name = "<td>%s</td>" % line['non_flying']
        remarks = "<td>%s</td>" % line['remarks']
            
        out = "<tr>" + date + name + remarks + "</tr>"
        
        return out
        
    def handle_records(self, line, submit=None):
        records = "<td>%s</td>" % line['records']
        out = "<tr>" + records + "</tr>"
        return out

    def handle_plane(self, line, submit=None):
        out = ["<tr>"]
        
        for field in ('tailnumber', 'type', 'manufacturer',
                      'model', 'cat_class', 'tags'):
                          
            out.append("<td class='%s'>%s</td>" % (field, line[field]))
            
        out.append("</tr>")
        
        return "".join(out)
        

###############################################################################


class DatabaseImport(PreviewImport):
                 
    def handle_flight(self, line):
        from forms import ImportFlightForm
        
        # get the plane based on the tailnumber and type, create if necessary
        kwargs = {"tailnumber": line.get("tailnumber"), "user": self.user}
        if line.get("type"):
            kwargs.update({"type": line.get("type")})
            
        plane, created = Plane.objects.get_or_create(**kwargs)
        line.update({"plane": plane.pk})
        
        flight = Flight(user=self.user)
        form = ImportFlightForm(line, instance=flight)
        
        if form.is_valid():
            form.save()
            message = 'good'
        else:
            message = form.errors
            
        return status_decorator(
            super(DatabaseImport, self).handle_flight, line, message
        )
        
    def handle_nonflight(self, line):
        from records.forms import NonFlightForm
        
        nf = NonFlight(user=self.user)
        
        form = NonFlightForm(line, instance=nf)
       
        if form.is_valid():
            form.save()
            message = 'good'
        else:
            message = form.errors
            
        return status_decorator(
            super(DatabaseImport, self).handle_nonflight, line, message
        )
            
    def handle_records(self, line):
        
        r, c = Records.objects.get_or_create(user=self.user)
        
        r.text = line['records']
        
        r.save()
                                          
        return super(DatabaseImport, self).handle_records(line)
        
    def handle_plane(self, line):
        
        p,c=Plane.objects.get_or_create(user=self.user,
                                        tailnumber=line['tailnumber'],
                                        type=line['type'])
        
        p.manufacturer = line['manufacturer']
        p.model = line['model']
        p.cat_class = line['cat_class']
        
        tags = line['tags']
        
        the_tags = []
        if tags:
            for tag in tags.split(","):
                tag = tag.strip()
                if tag.find(" ") > 0:
                    tag = "\"" + tag + "\""
                    
                the_tags.append(tag)
        
        p.tags = " ".join(the_tags)
        
        
        
        try:
            p.save()
            message = "good"
        except Exception, msg:
            message = msg
            
        return status_decorator(
            super(DatabaseImport, self).handle_plane, line, message
        )

def status_decorator(func, line, message):
    
    result = func(line)
    
    if message == 'good':
        result += """<tr class='good'><td colspan='20'>Line entered successfully
        </td></tr>"""
    else:
        result += """<tr class='bad'><td colspan='20'>The above line did not
        get entered because it had an error:<br>%s</td></tr>""" % message
    
    return result











































