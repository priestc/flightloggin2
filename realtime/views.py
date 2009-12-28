from annoying.decorators import render_to

@render_to('realtime.html')
def realtime(request):
    
    import datetime
    gmt = datetime.datetime.now() + datetime.timedelta(hours=5)
    
    from forms import DutyForm
    form = DutyForm()
    
    return locals()
