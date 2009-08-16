from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.contrib.auth.decorators import login_required

from annoying.decorators import render_to
from annoying.functions import get_object_or_None

from models import Plane
from forms import PlaneForm

@render_to('planes.html')
def planes(request):
    title="Planes"
    planes = Plane.objects.filter(user=request.user)
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
