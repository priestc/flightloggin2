from annoying.decorators import render_to
from annoying.functions import get_object_or_None
from models import Records
from forms import *
from is_shared import is_shared

@render_to("records.html")
def records(request, username):
    shared, display_user = is_shared(request, username)
    
    records,c = Records.objects.get_or_create(user=request.user)
    
    formset = NonFlightFormset(queryset=NonFlight.objects.filter(user=request.user))
    
    if request.POST:
        post = request.POST.copy()
        qs=NonFlight.objects.filter(user=request.user)
        
        for pk in range(0, qs.count()+1):
            post.update({"form-" + str(pk) + "-user": str(request.user.pk)})
            
        #assert False
            
        formset=NonFlightFormset(post, queryset=qs)
        if formset.is_valid():
            formset.save()
            
        records.text=request.POST.get('records')
        records.save()
        saved=True
    
    return locals()
