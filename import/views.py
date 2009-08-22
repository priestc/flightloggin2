from datetime import datetime
import re
import csv

from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect

from annoying.decorators import render_to
from annoying.functions import get_object_or_None

import settings
from forms import ImportForm, ImportFlightForm
from logbook.forms import NonFlightForm
from logbook.models import NonFlight, Flight
from plane.models import Plane
from route.models import Route
from records.models import Records
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
        line.update({"staging": True})
        
        #############################################
        
        instructor = line.get('instructor', "")
        student = line.get('student', "")
        captain = line.get('captain', "")
        fo = line.get('fo', "")
        
        person=""
        l = []
        if line.get('dual_r'):
            l = [instructor, captain, student, fo]
            
        if line.get('dual_g'):
            l = [student, fo, instructor, captain]
            
        if line.get('sic'):
            l = [captain, instructor, student, fo]
            
        if line.get('pic'):
            l = [fo, captain, instructor, student]

        for x in l:
            if x:
                person = x
                break

        #############################################
        
        if line.get('date')[:12] == "#####RECORDS": break
        
        if line.get('non_flying'):
            nf = NonFlight(user=request.user)
            form = NonFlightForm(line, instance=nf)
            
            if form.is_valid():
                form.save()
                out.append("good: nonflight")
        else:
            flight = Flight(user=request.user)
            plane, created = Plane.objects.get_or_create(tailnumber=line.get("tailnumber"), type=line.get("type"), user=request.user)
            line.update({"plane": plane.pk, "person": person})
            form = ImportFlightForm(line, instance=flight)
            
            if form.is_valid():
                form.save()
                out.append("good: " + line['date'] + line['tailnumber'])
            else:
                out.append(str(count) + "---------------------")
                out.append(form.errors)
                out.append(str(count) + "---------------------")


    if line.get('date')[:12] == "#####RECORDS":
        line = dr.next()
        r,c=Records.objects.get_or_create(user=request.user)
        r.text=line['date'].replace('\r', '\n')
        r.save()
    
    line = dr.next()        
    
    if line.get('date')[:11] == "#####PLANES":       
        for line in dr:
            tailnumber = line['date']
            manufacturer = line['tailnumber']
            model = line['type']
            type = line['route']
            cat_class = line['total']
            rt = line['pic']
            tags = line['solo']
            
            p=Plane.objects.get(user=request.user, tailnumber=tailnumber, type=type)
            p.manufacturer=manufacturer
            p.model=model
            p.cat_class=cat_class
            p.tags=tags
            
            print p.save()
        
            
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
    
        title = title.upper().strip().replace("\"", '').replace(".", "")
    
        if title in COLUMN_NAMES.keys():
            new.append(COLUMN_NAMES[title])
        else:
            new.append("??")
            
    return new














