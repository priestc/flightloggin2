from django.contrib.auth.decorators import login_required
from share.decorator import secret_key
from django.http import Http404, HttpResponse

from models import Location

################################

@secret_key
def clear(request):

    #select all locations that are owned by the common user (pk=1)
    airports = Location.objects.filter(user__id=1)
    c = airports.count()
    
    airports.delete()
    
    return HttpResponse("%s locations deleted" % c,
                        mimetype='text/plain')
