from annoying.decorators import render_to
from annoying.functions import get_object_or_None
from models import Records
from forms import *

@render_to("records.html")
def records(request):
    title="records"
    records,c = Records.objects.get_or_create(user=request.user)
    

    formset = NonFlightFormset(queryset=NonFlight.objects.filter(user=request.user))
    
    if request.POST:
        formset=NonFlightFormset(request.POST, queryset=NonFlight.objects.filter(user=request.user))
        if formset.is_valid():
            formset.save()
            
        records.text=request.POST.get('records')
        records.save()
        saved=True
    
    return locals()
