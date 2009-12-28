from django import template
from django.core.urlresolvers import reverse
from django.utils.safestring import mark_safe

register = template.Library()



@register.filter(name='list_users')
def list_users(users):
    "Lists all users, with an appropriate link and link color"

    out = ""  
    #return out


    for user in users:
        if user.get_profile().logbook_share:
            url = reverse('logbook', kwargs={"username": user.username})
            out += """<a href="%s" title="Click to see this user's logbook">%s</a>"""\
                    % (url, user.username)
               
        else:
            out += """<a title="This user does not allow othersto view his/her logbook"
                         class="noshare" href="">%s</a>""" % user.username
        
        out += ", "

    
    ## remove the last trailing ", "
    out = out[:-2]
    
    return mark_safe(out)
