from annoying.decorators import render_to

@render_to('maps.html')
def maps(request, shared, display_user):
    from settings import MEDIA_URL, SITE_URL, STATES_URL
    
    base_url = "%s/%s/%s/states-" % (SITE_URL,
                                     STATES_URL,
                                     display_user.username, )
    
    colored_url = "%s%s" % (base_url, "colored.png")
    unique_url = "%s%s" % (base_url, "unique.png")
    count_url = "%s%s" % (base_url, "count.png")
    
    return locals()
