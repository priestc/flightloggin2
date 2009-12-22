from django.contrib.auth.decorators import login_required
from annoying.decorators import render_to
from share.decorator import no_share
from django.http import HttpResponse

from models import Plane
from logbook.models import Flight
from forms import PopupPlaneForm

@render_to('planes.html')
def planes(request, shared, display_user):
    planes = Plane.objects.filter(user=display_user)
    form = PopupPlaneForm()
    changed = False
    
    if request.POST.get('submit') == "Create New Plane":
        plane = Plane(user=request.user)
        form = PopupPlaneForm(request.POST, instance=plane)      
        
        if form.is_valid():
            plane=form.save(commit=False)
            plane.user=request.user
            plane.save()
            changed = True
    
    elif request.POST.get('submit') == "Submit Changes":
        plane = Plane.objects.get(pk=request.POST.get("id"))
        form = PopupPlaneForm(request.POST, instance=plane)
        
        if form.is_valid():
            plane=form.save(commit=False)
            plane.user=request.user
            plane.save()
            changed = True
            
    elif request.POST.get('submit') == "Delete Plane":
        plane = Plane.objects.get(pk=request.POST.get("id"))
        
        if not plane.flight_set.all().count() > 0:
            plane.delete()
            changed = True
            
    if changed:
        from backup.models import edit_logbook
        edit_logbook.send(sender=display_user)
    
           
    return locals()


@no_share('NEVER')
@login_required()
@render_to('mass_planes.html')
def mass_planes(request, shared, display_user, page=0):
    from forms import PlaneFormset
    
    qs = Plane.objects.filter(user=display_user)
        
    if request.POST.get('submit'):
        formset = PlaneFormset(request.POST, queryset=qs)
        
        if formset.is_valid():
            formset.save()
            from django.http import HttpResponseRedirect
            from django.core.urlresolvers import reverse 
            url = reverse('planes', kwargs={"username": display_user.username})
            return HttpResponseRedirect(url)
            
            ## send signal so this user is marked as having edited
            ## their logbook for today
            from backup.models import edit_logbook
            edit_logbook.send(sender=display_user)
    
    else:
        formset = PlaneFormset(queryset=qs)
    
    return locals()

@render_to('plane_users.html')
def users(request, pk):
    from django.contrib.auth.models import User
    from airport.models import Location
    
    from django.db.models import Sum
    users = User.objects\
                .filter(profile__social=True)\
                .filter(flight__plane__tailnumber=pk)\
                .order_by()\
                .distinct()
    
    t_hours = Flight.objects\
                    .filter(plane__tailnumber=pk)\
                    .aggregate(s=Sum('total'))['s']
                    
    t_flights = Flight.objects.filter(plane__tailnumber=pk).count()
    
    t_airports = Location.objects\
                         .filter(routebase__land=True)\
                         .filter(routebase__route__flight__plane__tailnumber=pk)\
                         .order_by()\
                         .distinct()\
                         .count()
    
    return locals()
