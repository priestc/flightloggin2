import csv
import StringIO
import zipfile
import datetime

from logbook.constants import *

class Backup(object):

    def __init__(self, user):
        self.user=user
        
    def make_csv(self):
        """returns a StringIO representing a csv backup file for the user"""
        
        from records.models import Records
        from plane.models import Plane
        from logbook.models import Flight, Columns

        csv_sio = StringIO.StringIO()
        writer = csv.writer(csv_sio, delimiter="\t")
        
        ##########################
        
        writer.writerow([FIELD_TITLES[field] for field in BACKUP_FIELDS])
        
        flights = Flight.objects.filter(user=self.user)
        for flight in flights:
            writer.writerow([flight.column(field) for field in BACKUP_FIELDS])
        
        records = Records.goon(user=self.user)
        if records and records.text:
            writer.writerow(["##RECORDS", records.text.replace("\n","\\n")])
        
        planes = Plane.objects.filter(user=self.user)    
        for p in planes:
            writer.writerow(["##PLANES", p.tailnumber, p.manufacturer, p.model,
                        p.type, p.cat_class, ", ".join(p.get_tags())])
       
        self.csv = csv_sio
        return csv_sio

    def output_zip(self):
        """Outputs a zipfile containing the CSV file"""
        self.make_csv()
        
        DATE = datetime.date.today()
            
        zip_sio = StringIO.StringIO()
        z = zipfile.ZipFile(zip_sio,'w', compression=zipfile.ZIP_DEFLATED)
        z.writestr("logbook-backup-%s.tsv" % DATE, self.csv.getvalue())

        return zip_sio
