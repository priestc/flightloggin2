from annoying.decorators import render_to
from annoying.functions import get_object_or_None
from models import Records

@render_to("records.html")
def records(request):
    title="records"
    records,c = Records.objects.get_or_create(user=request.user)
    
    if request.POST:
        records.text=request.POST.get('records')
        records.save()
        saved=True
    
    return locals()
