import datetime

from flightloggin.share.decorator import no_share
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, Http404
from annoying.decorators import render_to

from classes import Backup, EmailBackup

@no_share('logbook')  
def backup(request):
    
    # get a zip file of the csv of the users data
    sio = Backup(request.display_user).output_zip()
    
    DATE = datetime.date.today()
    
    response = HttpResponse(sio.getvalue(), mimetype='application/zip')
    response['Content-Disposition'] = \
                'attachment; filename=logbook-backup-%s.tsv.zip' % DATE

    return response

#################################
#################################
#################################

@no_share('NEVER')
def emailbackup(request):
    """
    Send email backup to the user
    """
    
    email = EmailBackup(request.display_user)
    sent = email.send()
    
    return HttpResponse(sent, mimetype='text-plain')

@render_to('remove_email.html')
def change_email(request):
    u = request.GET.get('u')
    t = request.GET.get('t')
    
    from main.utils import hash_ten
    if not (u and t) or not (hash_ten(u) == t):
        raise Http404
    
    from django.contrib.auth.models import User
    user = User.objects.get(pk=u)

    p = user.get_profile()
    
    from profile.forms import ProfileForm
    form = ProfileForm(instance=p)
           
    
    return locals()

@render_to('remove_email.html')
def submit_change(request, userid):
    if request.POST:
        new_pref = request.POST['backup_freq']
        from profile.models import Profile
        p=Profile.objects.filter(user__pk=request.POST['u'])\
                         .update(backup_freq=new_pref)
        done=True
    
    return locals()

##
## crontab:
##
#30 5  1         * * wget -O - http://flightlogg.in/schedule-monthly.py?sk= > /root/month
#30 4  1,7,14,21 * * wget -O - http://flightlogg.in/schedule-weekly.py?sk= > /root/week
#30 3  1,14      * * wget -O - http://flightlogg.in/schedule-biweekly.py?sk= > /root/biweek
#59 23 *         * * wget -O - http://flightlogg.in/schedule-daily.py?sk= > /root/week
