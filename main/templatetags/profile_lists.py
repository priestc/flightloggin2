from django import template
from django.core.urlresolvers import reverse
from django.utils.safestring import mark_safe

register = template.Library()



@register.filter(name='list_users')
def list_users(users):
    "Lists all users, with an appropriate link and link color"
    
    if not users:
        return mark_safe("<em>None</em>")
    
    out = "" 

    for user in users:
        if user.get_profile().logbook_share:
            url = reverse('logbook', kwargs={"username": user.username})
            out += """<a href="%s" title="Click to see this user's logbook">%s</a>"""\
                    % (url, user.username)
               
        else:
            out += """<a title="This user does not allow others to view his/her logbook"
                         class="noshare" href="">%s</a>""" % user.username
        
        out += ", "

    
    ## remove the last trailing ", "
    out = out[:-2]
    
    return mark_safe(out)

###############################################################################

@register.filter(name='list_airports')
def list_airports(airports):
    
    if not airports:
        return mark_safe("<em>None</em>")
    
    out = ""
    for a in airports:
        ident = a.identifier
        url  = reverse('profile-airport', kwargs={"pk": ident})
        out += "<a href=\"%s\" title=\"%s\">%s</a>, "\
                     % (url, a.location_summary(), ident)
        
    ## remove the last trailing ", "
    out = out[:-2]
    
    return mark_safe(out)

###############################################################################

@register.filter(name='list_tailnumbers')
def list_airports(tailnumbers):
    
    if not tailnumbers:
        return mark_safe("<em>None</em>")
    
    out = ""
    for tn in tailnumbers:
        tn_spaceless = tn.replace(' ','')
        url  = reverse('profile-tailnumber', kwargs={"pk": tn_spaceless})
        out += "<a href=\"%s\">%s</a>, " % (url, tn)
        
    ## remove the last trailing ", "
    out = out[:-2]
    
    return mark_safe(out)

###############################################################################

@register.filter(name='list_types')
def list_types(types):
    
    if not types:
        return mark_safe("<em>None</em>")
    
    out = ""
    for ty in types:
        ty_spaceless = ty.replace(' ','')
        url  = reverse('profile-type', kwargs={"pk": ty_spaceless})
        out += "<a href=\"%s\">%s</a>, " % (url, ty)
        
    ## remove the last trailing ", "
    out = out[:-2]
    
    return mark_safe(out)

###############################################################################

@register.filter(name='routebase_row')
def routebase_row(rb):
    
    ident = rb.location.identifier
    
    if not rb.location or rb.custom():
        print "derp"
        return mark_safe("<td>%s</td><td>&nbsp;</td>" % ident)
        
    if rb.location.loc_class == 1:   # airport
        view = "profile-airport"
    elif rb.location.loc_class == 2:
        view = "profile-navaid"
        
    url = reverse(view, kwargs={"pk": ident})
    out = "<td><a href=\"%s\">%s</a></td>\n" % (url, ident)
    out += "<td>%s - %s</td>" % (rb.location.name, ident)
    
    return mark_safe(out)
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
