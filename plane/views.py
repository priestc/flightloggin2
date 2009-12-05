from django.contrib.auth.decorators import login_required
from annoying.decorators import render_to
from share.decorator import no_share

from models import Plane
from forms import PopupPlaneForm

@render_to('planes.html')
def planes(request, shared, display_user):
    planes = Plane.objects.filter(user=display_user)
    form = PopupPlaneForm()
    
    if request.POST.get('submit') == "Create New Plane":
        plane = Plane(user=request.user)
        form = PopupPlaneForm(request.POST, instance=plane)      
        
        if form.is_valid():
            plane=form.save(commit=False)
            plane.user=request.user
            plane.save()
    
    elif request.POST.get('submit') == "Submit Changes":
        plane = Plane.objects.get(pk=request.POST.get("id"))
        form = PopupPlaneForm(request.POST, instance=plane)
        
        if form.is_valid():
            plane=form.save(commit=False)
            plane.user=request.user
            plane.save()
            
    elif request.POST.get('submit') == "Delete Plane":
        plane = Plane.objects.get(pk=request.POST.get("id"))
        
        if not plane.flight_set.all().count() > 0:
            plane.delete()
            
            
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
            return HttpResponseRedirect('/%s/logbook.html' % display_user)
    else:
        formset = PlaneFormset(queryset=qs)
    
    return locals()
