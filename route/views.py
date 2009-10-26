from django.http import HttpResponse
from models import Route

def del_routes(request):
    if not request.user.is_staff:
        assert False
        
    count=Route.objects.filter(flight__pk__isnull=True).count()
    Route.objects.filter(flight__pk__isnull=True).delete()
    return HttpResponse("%s routes deleted" % count,
                        mimetype='text/plain')


def easy_recalc_routes(request):
    if not request.user.is_staff:
        assert False
        
    count = Route.easy_render_all()
    return HttpResponse("%s routes 'easy' recalculated" % count,
                        mimetype='text/plain')


def hard_recalc_routes(request):
    
    if not request.user.is_staff:
        assert False
        
    from django.contrib.auth.models import User
    count = 0
    for u in User.objects.all():
        count += 1
        Route.hard_render_user(user=u, no_dupe=True)
        
    return HttpResponse("%s routes 'hard' recalculated" % count,
                        mimetype='text/plain')
