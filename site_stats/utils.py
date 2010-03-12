from django.core.urlresolvers import reverse

def link_airports(lines):
    from airport.models import Location
    
    tem = '{number} <a title="{title}" href="{url}">{ident}</a> {value}\n'
    
    out = ""
    for line in lines[:-1]:
        s = line.split(" ")
        ident = s[1]
        
        title = Location.objects\
                        .get(identifier=ident, loc_class=1)\
                        .location_summary()
                        
        url = reverse('profile-airport', kwargs={"ident": ident})

        out += tem.format(number=s[0],
                         title=title,
                         url=url,
                         ident=ident,
                         value=s[2])
    
    return out

def link_tails(lines):
    
    tem = '{number} <a href="{url}">{tail}</a> {value}\n'
    
    out = ""
    for line in lines[:-1]:  ## the last one will be an empty string
        s = line.split(" ")
        tn = s[1]
        url = reverse('profile-tailnumber', kwargs={"tn": tn})
        out += tem.format(number=s[0], url=url, tail=tn, value=s[2])
        
    return out

def link_models(lines):
    
    tem = '{number} <a href="{url}">{model}</a> {value}\n'
    
    out = ""
    for line in lines[:-1]:
        s = line.split(" ")
        model = s[1]
        url = reverse('profile-model', kwargs={"model": model})
        # put the space back in instead of the underscore
        model = model.replace('_', ' ')
        out += tem.format(number=s[0], url=url, model=model, value=s[2])
    
    return out
