from django.core.paginator import Paginator, InvalidPage, EmptyPage
from annoying.decorators import render_to

from models import Plane
from forms import PlaneForm

@render_to('planes.html')
def planes(request, shared, display_user):
    planes = Plane.objects.filter(user=display_user)
    form = PlaneForm()
    
    if request.POST.get('submit') == "Create New Plane":
        plane = Plane(user=request.user)
        form = PlaneForm(request.POST, instance=plane)      
        
        if form.is_valid():
            plane=form.save(commit=False)
            plane.user=request.user
            plane.save()
    
    elif request.POST.get('submit') == "Submit Changes":
        plane = Plane.objects.get(pk=request.POST.get("id"))
        form = PlaneForm(request.POST, instance=plane)
        
        if form.is_valid():
            plane=form.save(commit=False)
            plane.user=request.user
            plane.save()
            
    elif request.POST.get('submit') == "Delete Plane":
        plane = Plane.objects.get(pk=request.POST.get("id"))
        
        if not plane.flight_set.all().count() > 0:
            plane.delete()
            
            
    return locals()
