from django.http import HttpResponse
from models import Route

def del_routes(request):
    count=Route.objects.filter(flight__pk__isnull=True).count()
    Route.objects.filter(flight__pk__isnull=True).delete()
    return HttpResponse("%s routes deleted" % count)

def recalc_routes(request):
    count = Route.render_all()
        
    return HttpResponse("%s routes recalculated" % count)
