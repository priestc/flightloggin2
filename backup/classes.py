import csv
import StringIO
import zipfile
import datetime

from django.http import Http404

from logbook.constants import *

MESSAGE = """This is a copy of your FlightLogg.in' logbook\n
You are set to receive these messages %s."""

class Backup(object):

    def __init__(self, user):
        self.user=user
        
    def output_csv(self):
        """returns a StringIO representing a csv backup file for the user"""
        
        from records.models import Records
        from plane.models import Plane
        from logbook.models import Flight, Columns
        from airport.models import Location

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
            writer.writerow(["##PLANE", p.tailnumber, p.manufacturer, p.model,
                        p.type, p.cat_class, ", ".join(p.get_tags())])
        
        locations = Location.objects.filter(user=self.user)
        for l in locations:
            
            try:
                x = l.location.x
                y = l.location.y
            except AttributeError:
                x, y = "", ""
            
            writer.writerow(["##LOC", l.identifier, l.name, x, y,
                    l.municipality, l.get_loc_type_display()])
       
        self.csv = csv_sio
        return csv_sio

    def output_zip(self):
        """Outputs a StringIO representing a zipfile containing the CSV file"""
        
        self.output_csv()
        
        DATE = datetime.date.today()
            
        zip_sio = StringIO.StringIO()
        z = zipfile.ZipFile(zip_sio,'w', compression=zipfile.ZIP_DEFLATED)
        z.writestr("logbook-backup-%s.tsv" % DATE, self.csv.getvalue())

        return zip_sio
    
class EmailBackup(object):
    
    def __init__(self, user):
        self.user = user
        from profile.models import Profile
        self.profile = Profile.get_for_user(user)
        
        self.addr = self.profile.backup_email or self.profile.user.email
        
        if not self.addr:
            raise Http404("No Email address to send to")
    
    def make_email(self):
        from django.core.mail import EmailMessage
        import datetime
        
        message = MESSAGE % self.profile.get_backup_freq_display().lower()
                            
        title = "%s's FlightLogg.in backup for %s" % (
                      self.profile.real_name or self.profile.user.username,
                      datetime.date.today()
        )
        
        file_ = Backup(self.user).output_zip().getvalue()
        
        email = EmailMessage(title, message, to=(self.addr,))
        email.attach("backup.tsv.zip", file_,)
            
        return email
    
    def send(self):
        """makes the email object, sends it, then, if successful, 
           returns the address it sent it to
        """
        sent = self.make_email().send()
        if sent:
            return self.addr
