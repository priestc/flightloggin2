from annoying.decorators import render_to
from forms import ProfileForm, ColumnsForm, AutoForm, UserForm
from models import *
from logbook.models import Columns
from logbook.constants import OPTION_FIELDS, FIELD_TITLES

@render_to("preferences.html")
def profile(request):
    title="Preferences"
    
    display_user = request.user
    profile = Profile.objects.get_or_create(user=request.user)[0]
    column =  Columns.objects.get_or_create(user=request.user)[0]
    auto =    AutoButton.objects.get_or_create(user=request.user)[0]
    
    #assert False
    
    if request.POST:
        profile_form = ProfileForm(request.POST, instance=profile)
        user_form = UserForm(request.POST, instance=display_user)
        column_form = ColumnsForm(request.POST, prefix="column", instance=column)
        auto_form = AutoForm(request.POST, prefix="auto", instance=auto)
    
        if auto_form.is_valid():
            auto_form.save()
            
        if profile_form.is_valid():
            profile_form.save()
            
        if column_form.is_valid():
            column_form.save()
         
        if user_form.is_valid():
            user_form.save()
        #else:
         #   assert False
        
    
    else:
        profile_form = ProfileForm(instance=profile)
        user_form = UserForm(instance=display_user)
        column_form = ColumnsForm(prefix="column", instance=column)
        auto_form = AutoForm(prefix="auto", instance=auto)
    
    bool_fields = []
    for field in OPTION_FIELDS:         ## mix the auto button and the columns fields into the same html table
        row = []
        
        row.append("<tr>\n")
        
        if auto_form.fields.get(field):
            row.append("<td>" + str(auto_form[field]) + "</td>\n")
        else:
            row.append("<td><input type='checkbox' style='visibility: hidden'></td>")
            
        if column_form.fields.get(field):
            row.append("<td>" + str(column_form[field]) + "</td>\n")
        
        row.append("<td>" + FIELD_TITLES[field] + "</td>\n")   
        row.append("</tr>\n")
        bool_fields.append("".join(row))

    return locals()
