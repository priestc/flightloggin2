from annoying.decorators import render_to

@render_to('realtime.html')
def realtime(request, shared, display_user):
    hi="ff"
    return locals()
