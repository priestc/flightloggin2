from datetime import datetime
import csv

from records.forms import NonFlightForm
from logbook.models import Flight
from records.models import Records, NonFlight
from plane.models import Plane

class BaseImport(object):
    def __init__(self, user, f):
        self.f = f
        self.user = user
        
        self.flight_out = []
        self.plane_out = []
        self.records_out = []
        self.non_out = []
        
        self.get_dict_reader()
        
    def do_pre(self):
        """get the first 10,000 characters of the file for preview purposes"""
        self.f.seek(0)
        self.pre = self.f.read(10000)
        self.f.seek(0)
        
    def save_file(self):
        filename = self.make_filename()
        dest = open(filename, 'wb+')
        
        for chunk in f.chunks():
            dest.write(chunk)
        dest.close()
        
    def get_dialect(self):
        self.do_pre()
        return csv.Sniffer().sniff(self.pre)
        
    def get_dict_reader(self):
        """makes a dictreader that is seek'd to the first valid line of data"""
        
        dialect = self.get_dialect()
        
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
        
        for line in self.dr:
            line_type, dic = PrepareLine(line).output()
            
            if line_type == "flight":
                self.handle_flight(dic)

            elif line_type == "nonflight":
                self.handle_nonflight(dic)
                
            elif line_type == "records":
                self.handle_records(dic)
                
            elif line_type == "plane":
                self.handle_plane(dic)
        
        #these variables get populated by the "handle_" methods
        return self.flight_out
    
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
        
        

###############################################################################

class PreviewImport(BaseImport):
        
    def make_filename(self):
        import settings
        filename = "%s/uploads/%s%s-p.txt" %\
                (settings.PROJECT_PATH,
                 datetime.now(),
                 self.user.username)

    def handle_flight(self, line, submit=None):
        
        out = ["<tr>"]
        from constants import PREVIEW_FIELDS
        for field in PREVIEW_FIELDS:
            out.append("<td class='%s'>%s</td>" % (field, line[field]))
            
        out.append("</tr>")
        
        # add the output of this line to the output list
        self.flight_out.append("".join(out))

    def handle_nonflight(self, line, submit=None):
        
        date = "<td>%s</td>" % line['date']
        name = "<td>%s</td>" % line['non_flying']
        remarks = "<td>%s</td>" % line['remarks']
            
        out = "<tr>" + date + name + remarks + "</tr>"
        
        self.non_out.append(out)
        
    def handle_records(self, line, submit=None):
        records = "<td>%s</td>" % line['records']
        out = "<tr>" + records + "</tr>"
        self.records_out.append(out)

    def handle_plane(self, line, submit=None):
        out = ["<tr>"]
        
        for field in ('tailnumber', 'type', 'manufacturer', 'model', 'tags'):
            out.append("<td class='%s'>%s</td>" % (field, line[field]))
            
        out.append("</tr>")
        
        self.plane_out.append("".join(out))
        

###############################################################################


class DatabaseImport(PreviewImport):
    
    def make_filename(self):
        """rename the file"""
        import settings
        filename = "%s/uploads/%s%s.txt" %\
                (settings.PROJECT_PATH,
                 datetime.now(),
                 self.user.username)
                 
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
            super(DatabaseImport, self).handle_flight(line)
        else:
            import pdb; pdb.set_trace()
            raise TypeError
        
    def handle_nonflight(self, line):
        from records.forms import NonFlightForm
        
        nf = NonFlight(user=self.user)
        
        form = NonFlightForm(line, instance=nf)
       
        if form.is_valid():
            form.save()
            super(DatabaseImport, self).handle_nonflight(line)
        else:
            import pdb; pdb.set_trace()
            raise TypeError
        
    def handle_records(self, line):
        
        r, c = Records.objects.get_or_create(user=self.user,
                                             text=line['records'])
                                          
        super(DatabaseImport, self).handle_records(line)
        
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
        p.save()
        
        super(DatabaseImport, self).handle_plane(line)












































