from django.http import HttpResponseRedirect

def redirect(request):
    """redirect any url with '.php' to the old PHP version"""
    
    return HttpResponseRedirect("http://old.flightlogg.in%s"\
                                             % request.get_full_path())

def redirect_to_forums(request):
    return HttpResponseRedirect("http://forums.flightlogg.in")
