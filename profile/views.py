from annoying.decorators import render_to
from forms import ProfileForm, ColumnsForm, AutoForm
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
        column_form = ColumnsForm(request.POST, prefix="column", instance=column)
        auto_form = AutoForm(request.POST, prefix="auto", instance=auto)
    
        if auto_form.is_valid() and profile_form.is_valid() and column_form.is_valid():
            auto_form.save()
            column_form.save()
            profile_form.save()
    
    else:
        profile_form = ProfileForm(instance=profile)
        column_form = ColumnsForm(prefix="column", instance=column)
        auto_form = AutoForm(prefix="auto", instance=auto)
    
    bool_fields = []
    for field in OPTION_FIELDS:
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
