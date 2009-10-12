from django.http import HttpResponse
from models import Route

def del_routes(request):
    count=Route.objects.filter(flight__pk__isnull=True).count()
    Route.objects.filter(flight__pk__isnull=True).delete()
    return HttpResponse("%s routes deleted" % count)

def easy_recalc_routes(request):
    count = Route.easy_render_all()
        
    return HttpResponse("%s routes 'easy' recalculated" % count)

def hard_recalc_routes(request):
    count = Route.hard_render_all('incrimental')
        
    return HttpResponse("%s routes 'hard' recalculated" % count)
