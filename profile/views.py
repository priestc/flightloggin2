import re

from forms import ProfileForm, ColumnsForm, AutoForm, UserForm
from models import *

from django.contrib.auth.decorators import login_required
from share.decorator import no_share
from annoying.decorators import render_to

from django.conf import settings

from plane.models import Plane
from logbook.models import Flight
from records.models import Records, NonFlight
from logbook.models import Columns
from airport.models import Location

from logbook.constants import OPTION_FIELDS, FIELD_TITLES

@no_share('NEVER')
@login_required
@render_to("preferences.html")
def profile(request):

    profile = Profile.objects.get_or_create(user=request.display_user)[0]
    column =  Columns.objects.get_or_create(user=request.display_user)[0]
    auto =    AutoButton.objects.get_or_create(user=request.display_user)[0]
    
    #assert False
    
    if request.POST:
        profile_form = ProfileForm(request.POST, instance=profile)
        user_form = UserForm(request.POST, instance=request.display_user)
        column_form = ColumnsForm(request.POST, prefix="column", instance=column)
        auto_form = AutoForm(request.POST, prefix="auto", instance=auto)
    
        if request.POST.get("submit") == "Delete All Flights":
            Flight.objects.filter(user=request.display_user).delete()
        
        elif request.POST.get("submit") == "Delete All Events":
            NonFlight.objects.filter(user=request.display_user).delete()
        
        elif request.POST.get("submit") == "Delete Unused Planes":
            Plane.objects.filter(flight__isnull=True, user=request.display_user).delete()
            
        elif request.POST.get("submit") == "Completely Reset All Data":
            NonFlight.objects.filter(user=request.display_user).delete()
            Flight.objects.filter(user=request.display_user).delete()
            Records.objects.filter(user=request.display_user).delete()
            Location.objects.filter(loc_class=3, user=request.display_user).delete()
            Plane.objects.filter(user=request.display_user).delete()
            
        else:
            if auto_form.is_valid():
                auto_form.save()
                
            if profile_form.is_valid():
                profile_form.save()
                
            if column_form.is_valid():
                column_form.save()
             
            if user_form.is_valid():
                ## remove illegal characters and spaces
                user = user_form.save(commit=False)
                user.username = \
                    re.sub(r'\W', '', user.username)\
                    .replace(" ",'')
                    
                print user.username
                 
                if request.display_user.id == settings.DEMO_USER_ID:
                    ## don't let anyone change the demo's username or email
                    ## it will break stuff
                    user_form.cleaned_data['username'] = 'demo'
                    user_form.cleaned_data['email'] = 'demo@what.com'
                
                #assert False, user.username
                user.save()        
    
    else:
        profile_form = ProfileForm(instance=profile)
        user_form = UserForm(instance=request.display_user)
        column_form = ColumnsForm(prefix="column", instance=column)
        auto_form = AutoForm(prefix="auto", instance=auto)
    
    
    f1 = '<td class="{cls}">{checkbox}</td>'
    f2 = '<td class="title">{title}</td><td class="description">{desc}</td>\n'
    
    
    bool_fields = []
    ## mix the auto button and the columns fields into the same html table
    ## FIXME: this should all be in a template tag
    for field in OPTION_FIELDS:
        row = []
        
        row.append("<tr>\n")
        
        if auto_form.fields.get(field):
            checkbox = str(auto_form[field])
        else:
            checkbox = "<input type='checkbox' style='visibility: hidden'>"
        
        row.append(f1.format(checkbox=checkbox, cls="aauto"))
            
        if column_form.fields.get(field):
            formatted = f1.format(checkbox=str(column_form[field]), cls="column")
            row.append(formatted)
        else:
            row.append('<td class="column"></td>')
        
        formatted = f2.format(title=FIELD_TITLES[field], desc=column_form[field].help_text)
        
        row.append(formatted)
                            
        row.append("</tr>\n")
        bool_fields.append("".join(row))

    return locals()
