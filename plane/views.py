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
    planeform = PlaneForm()
    return locals()
