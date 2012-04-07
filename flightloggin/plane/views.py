from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.db.models import Sum, Avg, Max

from annoying.decorators import render_to

from share.decorator import no_share
from logbook.models import Flight
from flightloggin.airport.models import Location
from flightloggin.route.models import Route

from models import Plane
from forms import PopupPlaneForm

@render_to('planes.html')
def planes(request):
    planes = Plane.objects.filter(user=request.display_user)
    form = PopupPlaneForm()
    changed = False
    
    if request.POST.get('submit') == "Create New Plane":
        plane = Plane(user=request.display_user)
        form = PopupPlaneForm(request.POST, instance=plane)      
        edit_or_new = "new"
        
        if form.is_valid():
            plane=form.save(commit=False)
            plane.user=request.display_user
            plane.save()
            changed = True
    
    elif request.POST.get('submit') == "Submit Changes":
        plane = Plane.objects.get(pk=request.POST.get("id"))
        form = PopupPlaneForm(request.POST, instance=plane)
        edit_or_new = "edit"
        
        if form.is_valid():
            plane=form.save(commit=False)
            plane.user=request.display_user
            plane.save()
            changed = True
            
    elif request.POST.get('submit') == "Delete Plane":
        plane = Plane.objects.get(pk=request.POST.get("id"))
        
        if not plane.flight_set.all().count() > 0:
            plane.delete()
            changed = True
            
    if changed:
        from backup.models import edit_logbook
        edit_logbook.send(sender=request.display_user)
    
           
    return locals()


@no_share('NEVER')
@login_required()
@render_to('mass_planes.html')
def mass_planes(request, page=0):
    from forms import PlaneFormset
    
    qs = Plane.objects.filter(user=request.display_user)
        
    if request.POST.get('submit'):
        formset = PlaneFormset(request.POST, queryset=qs)
        
        if formset.is_valid():
            formset.save()
            from django.http import HttpResponseRedirect
            from django.core.urlresolvers import reverse 
            url = reverse('planes', kwargs={"username": request.display_user.username})
            return HttpResponseRedirect(url)
            
            ## send signal so this user is marked as having edited
            ## their logbook for today
            from backup.models import edit_logbook
            edit_logbook.send(sender=request.display_user)
    
    else:
        formset = PlaneFormset(queryset=qs)
    
    return locals()


###############################################################################

@render_to('tailnumber_profile.html')
def tailnumber_profile(request, tn):
    
    types = Plane.objects\
                 .filter(hidden=False)\
                 .filter(tailnumber__iexact=tn)\
                 .values_list('type', flat=True)\
                 .exclude(type="")\
                 .order_by()\
                 .distinct()
                 
    models = Plane.objects\
                 .filter(hidden=False)\
                 .filter(tailnumber__iexact=tn)\
                 .values_list('model', flat=True)\
                 .exclude(model="")\
                 .order_by()\
                 .distinct()
    
    users = Plane.get_profiles(tailnumber=tn)
    
    t = Flight.objects\
              .filter(plane__tailnumber__iexact=tn)\
              .filter(plane__hidden=False)\
                    
    t_hours = t.aggregate(s=Sum('total'))['s']             
    t_flights = t.count()
    
    routes = Route.objects.filter(flight__plane__tailnumber=tn,
                                  flight__plane__hidden=False)
    
    return locals()

@render_to('type_profile.html')
def type_profile(request, ty):
    
    ## the users who have flown this type
    users = Plane.get_profiles(type=ty)
    
    t_hours = Flight.objects\
                    .filter(plane__type__iexact=ty)\
                    .aggregate(s=Sum('total'))['s'] 
    
    t_flights = Flight.objects.filter(plane__type__iexact=ty).count()
    
    u_airports = Location.objects\
                         .filter(routebase__route__flight__plane__type__iexact=ty,
                                 loc_class__lte=2)\
                         .order_by()\
                         .distinct()\
                         .count()
    
    tailnumbers = Plane.objects\
                       .values_list('tailnumber', flat=True)\
                       .filter(type__iexact=ty)\
                       .order_by()\
                       .distinct()
    
    return locals()

@render_to('model_profile.html')
def model_profile(request, model):
    
    url_model = model
    model = model.replace('_', ' ')
    
    ## the users who have flown this type
    users = Plane.get_profiles(model=model)
    
    # total hours in model
    t_hours = Flight.objects\
                    .filter(plane__model__iexact=model)\
                    .aggregate(s=Sum('total'))['s'] 
    
    # total flights in model
    t_flights = Flight.objects.filter(plane__model__iexact=model).count()
    
    # unique airports
    u_airports = Location.objects\
                         .filter(routebase__route__flight__plane__model__iexact=model,
                                 loc_class__lte=2)\
                         .order_by()\
                         .distinct()\
                         .count()
    
    # tailnumbers of this model
    tailnumbers = Plane.objects\
                       .values_list('tailnumber', flat=True)\
                       .filter(model__iexact=model)\
                       .order_by()\
                       .distinct()
    
    avg_speed = Flight.objects\
                      .user('ALL')\
                      .filter(plane__model__iexact=model)\
                      .exclude(speed__lte=30)\
                      .exclude(app__gt=1)\
                      .exclude(route__total_line_all__lt=50)\
                      .aggregate(s=Avg('speed'))['s'] 
                      
    
    return locals()

@render_to('search_tailnumbers.html')
def search_tailnumbers(request):

    if not request.GET:
        return locals()
    
    from django.db.models import Q
    
    s = request.GET.get('q')
    
    results = Plane.objects\
                   .filter(tailnumber__icontains=s)\
                   .values('manufacturer', 'tailnumber', 'type', 'model')\
                   .distinct()\
                   .order_by('tailnumber')
    
    count = results.count()
    did_something = True
    
    return locals()
