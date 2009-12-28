import datetime

from share.decorator import no_share, secret_key
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
    """Send email backup to the user"""
    
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

@secret_key
def schedule(request, schedule):
    """Only send out the emails to the people who's schedule is exactly the
       one being passed as 'schedule'
    """
    
    from django.contrib.auth.models import User
    if schedule == 'weekly':
        users = User.objects.filter(profile__backup_freq=1)
    
    elif schedule == 'biweekly':
        users = User.objects.filter(profile__backup_freq=2)
    
    elif schedule == 'monthly':
        users = User.objects.filter(profile__backup_freq=3)
        
    elif schedule == 'daily':
        today = datetime.date.today()
        users = User.objects.filter(profile__backup_freq=4,
                                    userstoday__date=today
                                   )
    
    ret = "%s - %s \n\n" % (schedule, datetime.datetime.now())    
    for user in users:
        em = EmailBackup(user, auto=True)
        result = em.send(test=False)
        ret += "%s [%s]\n" % (user.username, result)
    
    
    return HttpResponse(ret, mimetype="text/plain")

##
## crontab:
##
#30 5  1         * * wget http://flightlogg.in/schedule-monthly.py?sk=
#30 4  1,7,14,21 * * wget http://flightlogg.in/schedule-weekly.py?sk=
#30 3  1,14      * * wget http://flightlogg.in/schedule-biweekly.py?sk=
#59 23 *         * * wget http://flightlogg.in/schedule-daily.py?sk=
