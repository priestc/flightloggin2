import csv
import cStringIO
import zipfile
import datetime

from django.http import Http404

from logbook.constants import *

MESSAGE = """This is a copy of your FlightLogg.in' logbook\n
You are set to receive these messages %s.\n\n"""

REMOVE = """Go here to change email preferences:
http://flightlogg.in/change_email.html?u=%s&t=%s"""

class Backup(object):

    def __init__(self, user):
        self.user=user
        
    def output_csv(self):
        """returns a StringIO representing a csv backup file for the user"""
        
        from records.models import Records, NonFlight
        from plane.models import Plane
        from logbook.models import Flight, Columns
        from airport.models import Location

        csv_sio = cStringIO.StringIO()
        writer = csv.writer(csv_sio, delimiter="\t")
        
        ##########################
        
        writer.writerow([FIELD_TITLES[field] for field in BACKUP_FIELDS])
        
        flights = Flight.objects.filter(user=self.user)
        for flight in flights:
            tmp=[]
            for field in BACKUP_FIELDS:
                try:
                    try:
                        s = str(flight.column(field))
                    except:
                        s = flight.column(field).encode("utf-8", "ignore")
                    tmp.append(s)
                except Exception, e:
                    tmp.append("error (%s): %s" % (e, flight.id))
                
            writer.writerow(tmp)
        
        records = Records.goon(user=self.user)
        if records and records.text:
            writer.writerow(["##RECORDS", records.text.replace("\n","\\n")])
        
        planes = Plane.objects.filter(user=self.user)    
        for p in planes:
            writer.writerow(["##PLANE", p.tailnumber, p.manufacturer, p.model,
                        p.type, p.cat_class, "X", ", ".join(p.get_tags()),
                        p.description])
                        
        events = NonFlight.objects.filter(user=self.user)    
        for e in events:
            writer.writerow(["##EVENT", e.date, e.non_flying, e.remarks])
        
        locations = Location.objects.filter(user=self.user)
        for l in locations:
            
            try:
                x = l.location.x
                y = l.location.y
            except AttributeError:
                x, y = "", ""
            
            writer.writerow(["##LOC", l.identifier, l.name, x, y,
                    l.municipality, l.get_loc_type_display()])
                    
        #save to self.csv before returning, for later use
        self.csv = csv_sio
        
        return csv_sio

    def output_zip(self):
        """Outputs a StringIO representing a zipfile containing the CSV file"""
        
        self.output_csv()
        
        DATE = datetime.date.today()
            
        zip_sio = cStringIO.StringIO()
        z = zipfile.ZipFile(zip_sio,'w', compression=zipfile.ZIP_DEFLATED)
        z.writestr("logbook-backup-%s.tsv" % DATE, self.csv.getvalue())

        return zip_sio
    
class EmailBackup(object):
    
    def __init__(self, user, auto=False):
        
        self.auto = auto

        self.user = user
        from profile.models import Profile
        self.profile,c = Profile.objects.get_or_create(user=user)
        
        self.addr = self.profile.backup_email or self.profile.user.email
    
    def make_email(self):
        from django.core.mail import EmailMessage
        import datetime

        today = datetime.date.today()
        
        message = MESSAGE % self.profile.get_backup_freq_display().lower()
        
        from main.utils import hash_ten
        token = hash_ten(self.user.id)
        
        message += REMOVE % (self.user.id, token)
                            
        title = "%s's FlightLogg.in backup for %s" % (
                      self.profile.real_name or self.profile.user.username,
                      today
        )
        
        #import pdb; pdb.set_trace()
        
        file_ = Backup(self.user).output_zip().getvalue()
        
        if self.auto:
            f = "Auto Backup Mailer <info@flightlogg.in>"
        else:
            f = "Manual Backup Mailer <info@flightlogg.in>"

        email = EmailMessage(title, message, to=(self.addr,), from_email=f)
        email.attach("backup-%s.tsv.zip" % today, file_,)
            
        return email
    
    def send(self, test=False):
        """makes the email object, sends it, then, if successful, 
           returns the address it sent it to
        """
        
        from django.conf import settings
        if self.user.id == settings.DEMO_USER_ID:
            return """e-mail backups disabled for the demo account, please register an account to use this feature"""
        
        if not self.addr:
            return "--No e-mail to send to--"
        
        em = self.make_email()
        
        if not test:
            sent = em.send()
            return "e-mail sent to: %s" % (self.user, self.addr)
        else:
            return "test: %s" % self.user



