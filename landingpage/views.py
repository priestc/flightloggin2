import base64
import hashlib
import hmac
import simplejson as json
import random
import string

from django.template.response import TemplateResponse
from django.conf import settings
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.core.mail import EmailMessage
from django.views.decorators.cache import cache_page

from profile.models import Profile
from site_stats.models import StatDB
from forms import RegistrationForm

@cache_page(5 * 60 * 60)
def landingpage(request):

    stats = StatDB.objects.latest()

    if request.user.is_authenticated():
        url = reverse('logbook', args=[request.user.username])
        return HttpResponseRedirect(url)

    if request.POST:
        form = RegistrationForm(request.POST)
        if form.is_valid():
            p = form.register()
            password = form.cleaned_data['password']
            user = authenticate(username=p.user.username, password=password)
            login(request, user)
            url = reverse('logbook', args=[request.user.username])
            return HttpResponseRedirect(url)
    else:
        form = RegistrationForm()
    return TemplateResponse(request, 'landingpage.html', locals())

def registration(request):
    """
    Handle the data coming in from the register form on the landingpage
    """
    if request.POST['signed_request']:
        return fb_registration_callback(request)
    
    register_form = RegisterForm(request.POST)
    if register_form.is_valid():
        user = register_form.save()

    return HttpResponseRedirect('/%s' % user.username)

def reset_password(request):
    if request.POST:
        data = request.POST['data']
        if "@" in data:
            o = {'email': data}
        else:
            o = {'username': data}

        users = User.objects.filter(**o)
        if not users.exists():
            messages.error(request, 'Email or username could not be found')
        else:
            for u in users:
                try:
                    #send_reset_email(u)
                    print u
                except Exception:
                    messages.error('No email attached to account %' % data)
                messages.info(request, 'Email sent to %s for user %s' % (u.email, u.username))

    return TemplateResponse(request, 'reset_password.html', locals())

def new_login(request):
    """
    Handle data coming in from the login box on the landingpage
    """
    username = request.POST.get('login_username')
    password = request.POST.get('login_password')

    if not request.POST or not (username and password):
        return HttpResponseRedirect(reverse('landingpage'))
    
    user = authenticate(username=username, password=password)
    if user is None:
        messages.error(request, 'Username/password incorrect')
        return HttpResponseRedirect(reverse('landingpage'))

    login(request, user)
    return HttpResponseRedirect(reverse('logbook', args=[request.user.username]))

def fb_registration_callback(request):
    """
    This view only gets hit by the facebook callback when a user registers.
    """
    signed_request = request.POST['signed_request']
    response = parse_signed_request(signed_request, settings.FACEBOOK_SECRET)
    data = response['registration']
    
    u = User(
        username=data['username'],
        email=data['email'],
        first_name=data['first_name'],
        last_name=data['last_name'],
    )
    
    d, m, y = data['birthday'].split('/')
    dob = datetime.datetime(year=y, month=m, date=d)
    
    p = Profile(
        user=u,
        dob=dob,
    )
    
    print response


def send_reset_email(user):
    char_set = string.ascii_uppercase + string.digits
    password = ''.join(random.sample(char_set,10))
    user.set_password(password)
    user.save()

    title = "FlightLoggin' password reset"
    message = """You requested a password reset.\n
    Password: {0}\nUsername: {1}\n
    http://flightlogg.in"""

    message = message.format(password, user.username)

    email = user.email or email.get_profile().backup_email

    if not email:
        raise Exception('No email')

    email = EmailMessage(
        title,
        message,
        to=(user.email,),
        from_email='info@flightlogg.in',
    )
    email.send()


def base64_url_decode(inp):
    padding_factor = (4 - len(inp) % 4) % 4
    inp += "="*padding_factor 
    return base64.b64decode(unicode(inp).translate(dict(zip(map(ord, u'-_'), u'+/'))))

def parse_signed_request(signed_request, secret):
    l = signed_request.split('.', 2)
    encoded_sig = l[0]
    payload = l[1]

    sig = base64_url_decode(encoded_sig)
    data = json.loads(base64_url_decode(payload))

    if data.get('algorithm').upper() != 'HMAC-SHA256':
        log.error('Unknown algorithm')
        return None
    else:
        expected_sig = hmac.new(secret, msg=payload, digestmod=hashlib.sha256).digest()

    if sig != expected_sig:
        return None
    else:
        return data