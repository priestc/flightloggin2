import datetime

from django.contrib.auth.decorators import login_required

from annoying.functions import get_object_or_None
from profile.models import Profile

from logbook.constants import *
from profile.models import Profile
from is_shared import is_shared

@login_required()   
def backup(request, username):
    from django.http import HttpResponse
    shared, display_user = is_shared(request, username)
    date = datetime.date.today()
    
    sio = backup_zip(display_user)
    
    ###########################
    
    response = HttpResponse(sio, mimetype='application/zip')
    response['Content-Disposition'] = 'attachment; filename=logbook-backup-%s.csv.zip' % date

    return response
    
def backup_zip(user):
    """returns a StringIO representing a zipped backup file for the passed user instance"""
    
    import csv, zipfile, StringIO
    from records.models import Records
    from plane.models import Plane
    from logbook.models import Flight, Columns

    date = datetime.date.today()
    output = StringIO.StringIO()
    writer = csv.writer(output, dialect='excel')
    
    ##########################
    
    writer.writerow([FIELD_TITLES[field] for field in BACKUP_FIELDS])
    
    flights = Flight.objects.filter(user=user)
    for flight in flights:
        writer.writerow([flight.column(field) for field in BACKUP_FIELDS])
        
    writer.writerow(["##RECORDS"])
    
    records = get_object_or_None(Records, user=user)
    if records:
        writer.writerow([records.text.replace("\n","\\n")])
    else:
        writer.writerow([])
        
    writer.writerow(["##PLANES"])
    
    planes = Plane.objects.filter(user=user)    
    for p in planes:
        writer.writerow([p.tailnumber, p.manufacturer, p.model, p.cat_class, " ".join(p.get_tags_quote())])
    
    sio = StringIO.StringIO()
    z = zipfile.ZipFile(sio,'w', compression=zipfile.ZIP_DEFLATED)
    z.writestr("logbook-backup-%s.csv" % date, output.getvalue())
       
    return sio

def emailbackup(response, group):
    """Automatically send email backups to each user"""
    from django.core.mail import EmailMessage, SMTPConnection, send_mail
    import datetime
    
    assert group > 0
    
    profiles = Profile.objects.filter(backup_freq__lte=group).exclude(backup_freq=0)
    
    emails = []
    for profile in profiles:
        message = ("This is a copy of your FlightLogg.in' logbook\nYou are set to receive these messages %s." %
                            profile.get_backup_freq_display().lower() )
                            
        title = "%s's FlightLogg.in backup for %s" % (profile.real_name or profile.user.username, datetime.date.today(), )
        email = profile.backup_email or profile.user.email
        
        file_ = backup_zip(profile.user).getvalue()
        
        email = EmailMessage(title, message, to=(email,))
        email.attach("backup.csv.zip", file_,)
        emails.append(email)
        
    connection = SMTPConnection()
    connection.send_messages(emails)
        
    assert False















    
