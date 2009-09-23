from django.http import HttpResponseRedirect

def redirect(request):
    """redirect any url with '.php' to the old PHP version"""
    
    return HttpResponseRedirect("http://old.flightlogg.in" + request.get_full_path())
