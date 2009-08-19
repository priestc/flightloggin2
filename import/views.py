from datetime import datetime
import re
import csv

from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect

from annoying.decorators import render_to
from annoying.functions import get_object_or_None
import settings
from forms import ImportForm
from logbook.forms import FlightForm

@render_to('import.html')
def do_import(request, f):
    reader = csv.reader(f, delimiter="\t")
    
    titles = reader.next()
    reader = csv.DictReader(f, titles)
    assert False
    out = []
    count = 0
    
    for line in reader:
        count += 1
        line.update({"staging": True, "user": request.user.id})
        form = FlightForm(line)
        if form.is_valid():
            form.save()
            out.append("good: " + line['Date'])
        else:
            out.append("bad: " + line['Date'])
            
    del form
            
    return locals()

@render_to('import.html')
def import_s(request):
    title = "Import/Export"
    
    if request.method == 'POST':
        form = ImportForm(request.POST, request.FILES)
        if form.is_valid():
            filename = "%s/uploads/%s_%s.txt" % (settings.PROJECT_PATH, request.user.id, datetime.now())
            f = request.FILES['file']
            destination = open( filename , 'wb+')
            
            for chunk in f.chunks():
                destination.write(chunk)
            destination.close()
            
            return do_import(request, f)
    else:
        form = ImportForm()
        
    return locals()
