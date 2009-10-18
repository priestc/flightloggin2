from django.http import Http404
from django.contrib.auth.decorators import login_required
from share.decorator import no_share

from annoying.decorators import render_to

from profile.models import Profile
from logbook.constants import *

import datetime
DATE = datetime.date.today()

@login_required()   
def backup(request, shared, display_user):
    from django.http import HttpResponse
    from classes import Backup
    
    # get a zip file of the csv of the users data
    sio = Backup(display_user).output_zip()

    ###########################
    
    response = HttpResponse(sio.getvalue(), mimetype='application/zip')
    response['Content-Disposition'] = 'attachment; filename=logbook-backup-%s.tsv.zip' % DATE

    return response

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















    
