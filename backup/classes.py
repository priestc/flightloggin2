import csv
import cStringIO
import zipfile
import datetime

from django.core.mail import EmailMessage
from django.http import Http404
from django.conf import settings

from logbook.constants import *
from records.models import Records, NonFlight
from plane.models import Plane
from logbook.models import Flight, Columns
from airport.models import Location
from profile.models import Profile

from main.utils import hash_ten

class Backup(object):
    """
    Constructor takes one argument, an instance of the User object
    """
    def __init__(self, user):
        self.user = user
        
    def output_csv(self):
        """returns a StringIO representing a csv backup file for the user"""

        csv_sio = cStringIO.StringIO()
        writer = csv.writer(csv_sio, delimiter="\t")
        
        ##########################
        
        writer.writerow([FIELD_TITLES[field] for field in BACKUP_FIELDS])
        
        flights = Flight.objects.filter(user=self.user).order_by('date')
        for flight in flights:
            tmp=[]
            for field in BACKUP_FIELDS:
                try:
                    ## nested try blocks are ugly, but this is the only
                    ## way to have a way to make dates and unicode characters
                    ## both made into strings
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
            rec = records.text.encode("utf-8", "ignore").replace("\n","\\n")
            writer.writerow(["##RECORDS", rec])
        
        planes = Plane.objects.filter(user=self.user)    
        for p in planes:
            tags = ", ".join(p.get_tags_quote())
            writer.writerow(["##PLANE", p.tailnumber, p.manufacturer, p.model,
                        p.type, p.cat_class, "X", tags,
                        p.description, p.fuel_burn])
                        
        events = NonFlight.objects.filter(user=self.user)    
        for e in events:
            writer.writerow(["##EVENT", e.date, e.non_flying, e.remarks.encode("utf-8", "ignore")])
        
        locations = Location.objects.filter(user=self.user)
        for l in locations:
            x = getattr(l.location, "x", "")
            y = getattr(l.location, "y", "")
            
            writer.writerow(["##LOC", l.identifier, l.name, x, y,
                    l.municipality, l.get_loc_type_display()])
                    
        #save to self.csv before returning, for potential later use
        self.csv = csv_sio
        
        return csv_sio

    def output_zip(self):
        """
        Outputs a StringIO representing a zipfile containing the CSV file
        """
        
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
        self.profile,c = Profile.objects.get_or_create(user=user)
        
        self.addr = self.profile.backup_email or self.profile.user.email
    
    def make_unsubscrbe_link(self):        
        token = hash_ten(self.user.id)
        url = "http://flightlogg.in/change_email.html?u=%s&t=%s"
        
        return url % (self.user.id, token)
    
    def make_email(self):
        today = datetime.date.today()
        
        unsub = self.make_unsubscrbe_link()
        
        message = """This is a copy of your FlightLogg.in' logbook"""
        
        message += "\nYou are set to receive these messages %s." %\
                        self.profile.get_backup_freq_display().lower()
                    
        message += "\n\nGo here to change email preferences: %s" %\
                        unsub
        
        ####~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                            
        title = "%s's FlightLogg.in backup for %s" %\
                (self.profile.real_name or self.profile.user.username, today)
        
        #import ipdb; ipdb.set_trace()
        
        file_ = Backup(self.user).output_csv().getvalue()
        
        if self.auto:
            f = "Auto Backup Mailer <info@flightlogg.in>"
        else:
            f = "Manual Backup Mailer <info@flightlogg.in>"

        email = EmailMessage(title,
                             message,
                             to=(self.addr,),
                             from_email=f,
                             headers={"List-Unsubscribe": unsub})
                             
        email.attach("backup-%s.tsv" % today, file_,)
            
        return email
    
    def send(self, test=False):
        """
        Makes the email object, sends it, then, if successful, 
        returns the address it sent it to
        """
        if self.user.id == settings.DEMO_USER_ID:
            return """e-mail backups disabled for the demo account, please register an account to use this feature"""
        
        if not self.addr:
            return "--No e-mail to send to--"
        
        em = self.make_email()
        
        if not test:
            sent = em.send()
            return "e-mail sent to: %s" % self.addr
        else:
            return "test: %s" % self.user



