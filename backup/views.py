import datetime

from django.http import Http404
from django.contrib.auth.decorators import login_required
from share.decorator import no_share

from annoying.decorators import render_to
from annoying.functions import get_object_or_None

from profile.models import Profile
from logbook.constants import *

DATE = datetime.date.today()

@login_required()   
def backup(request, shared, display_user):
    from django.http import HttpResponse
   
    sio = backup_zip(display_user)

    ###########################
    
    response = HttpResponse(sio.getvalue(), mimetype='application/zip')
    response['Content-Disposition'] = 'attachment; filename=logbook-backup-%s.tsv.zip' % DATE

    return response
    
def backup_csv(user):
    """returns a StringIO representing a csv backup file for the passed user instance"""
    
    import csv, StringIO
    from records.models import Records
    from plane.models import Plane
    from logbook.models import Flight, Columns

    csv_sio = StringIO.StringIO()
    writer = csv.writer(csv_sio, dialect='excel')
    
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
   
    return csv_sio

def backup_zip(user):
    import zipfile, StringIO
    
    csv_sio = backup_csv(user)
        
    zip_sio = StringIO.StringIO()
    z = zipfile.ZipFile(zip_sio,'w', compression=zipfile.ZIP_DEFLATED)
    z.writestr("logbook-backup-%s.tsv" % DATE, csv_sio.getvalue())

    return zip_sio

#################################
#################################
#################################

@no_share
@login_required() 
def emailbackup(request, shared, display_user):
    """Send email backup to the user"""
    
    profile = Profile.objects.get(user=display_user)
    
    email = make_email(profile)
    sent=email.send()
    
    from django.http import HttpResponse
    return HttpResponse("email sent to %s" % ",".join(email.to), mimetype='text-plain')
    

def make_email(profile):
    from django.core.mail import EmailMessage, SMTPConnection, send_mail
    import datetime
    
    message = ("This is a copy of your FlightLogg.in' logbook\nYou are set to receive these messages %s." %
                        profile.get_backup_freq_display().lower() )
                        
    title = "%s's FlightLogg.in backup for %s" % (profile.real_name or profile.user.username, datetime.date.today(), )
    email = profile.backup_email or profile.user.email
    
    file_ = backup_zip(profile.user).getvalue()
    
    email = EmailMessage(title, message, to=(email,))
    email.attach("backup.tsv.zip", file_,)
        
    return email















    
