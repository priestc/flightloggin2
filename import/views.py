from datetime import datetime
import re
import csv

from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect

from annoying.decorators import render_to
from annoying.functions import get_object_or_None

import settings
from forms import ImportForm
from logbook.forms import FlightForm, NonFlightForm
from logbook.models import NonFlight, Flight
from plane.models import Plane
from constants import COLUMN_NAMES

@render_to('import.html')
def do_import(request, f):

    reader = csv.reader(f, delimiter='\t')
    titles = reader.next()
    titles = swap_out_titles(titles)
    dr = csv.DictReader(f, titles, delimiter='\t')
    dr.next()
    out = []
    count = 0
    
    for line in dr:
        count += 1
        if count > 15: break
        line.update({"staging": True})
        #assert False
        
        if line.get('non_flying'):
            nf = NonFlight(user=request.user)
            form = NonFlightForm(line, instance=nf)
        else:
            flight = Flight(user=request.user)
            plane, created = Plane.objects.get_or_create(tailnumber=line.get("tailnumber"), type=line.get("type"), user=request.user)
            route = line.get("route")
            line.update({"plane": plane.pk})
            form = FlightForm(line, instance=flight)
            
        if form.is_valid():
            form.save()
            out.append("good: " + line['date'] + line['route'] + line['tailnumber'])
        else:
            out.append(line)
            out.append(str(count) + "---------------------")
            
    #del form
            
    return locals()

@render_to('import.html')
def import_s(request):
    title = "Import/Export"
    
    if request.method == 'POST':
        fileform = ImportForm(request.POST, request.FILES)
        if fileform.is_valid():
            filename = "%s/uploads/%s_%s.txt" % (settings.PROJECT_PATH, request.user.id, datetime.now())
            f = request.FILES['file']
            destination = open( filename , 'wb+')
            
            for chunk in f.chunks():
                destination.write(chunk)
            destination.close()
            
            return do_import(request, f)
    else:
        fileform = ImportForm()
        
    return locals()
    
def swap_out_titles(original):
    new = []
    for title in original:
    
        title = title.upper().strip().replace("\"", '')
    
        if title in COLUMN_NAMES.keys():
            new.append(COLUMN_NAMES[title])
        else:
            new.append("??")
            
    return new














