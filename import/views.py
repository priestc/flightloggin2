from datetime import datetime
import re
import csv

import settings
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect

from annoying.decorators import render_to
from annoying.functions import get_object_or_None

from logbook.constants import DB_FIELDS
from logbook.forms import NonFlightForm
from logbook.models import NonFlight, Flight
from records.models import Records

from constants import COLUMN_NAMES
from forms import ImportForm, ImportFlightForm

@render_to('import.html')
def do_import(request, f, preview=True):

    reader = csv.reader(f, delimiter='\t')
    titles = reader.next()
    titles = swap_out_flight_titles(titles)
    dr = csv.DictReader(f, titles, delimiter='\t')
    dr.next()
    out = []
    count = 0
    
    for line in dr:
        count += 1
        
        line_type, line = prepare_line(line)

        if line_type == "FLIGHT":
            print "flight " + str(count)
            if preview:
                out = make_preview_flight(line, out)
            else:
                out = make_commit_flight(line, request.user, out)

        elif line_type == "NON-FLIGHT":
            print "non-flight " + str(count)
            if preview:
                out = make_preview_nonflight(line, out)
            else:
                out = make_commit_nonflight(line, request.user, out)

        elif line_type == "PLANE":
            print "plane " + str(count)
            if preview:
                out = make_preview_plane(line, out)
            else:
                out = make_commit_plane(line, request.user, out)

        elif line_type == "RECORDS":
            print "records " + str(count)
            if preview:
                out = make_preview_records(line['date'], out)
            else:
                out = make_commit_records(line['date'], request.user, out)
            
    return {"out": out}

#########################################################################################

def prepare_line(line):
    if line.get('non_flying'):
        return "NON-FLIGHT", line
        
    if line.get('date')[:12] == "##Records":
        return "RECORDS", line
        
    if line.get('date')[:11] == "##Tailnumber":
        return "PLANE", line
        
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

    return "FLIGHT", line

###############################################

def make_preview_flight(line, out):
    row = ["<td>" + line[field] + "</td>" for field in DB_FIELDS]
    out.append("<tr>" + "".join(row) + "</tr>")
    return out
    
def make_preview_nonflight(line, out):
    row = ["<td>" + line[field] + "</td>" for field in ['date', 'non_flying']]
    out.append("<tr colspan='20'>" + "".join(row) + "</tr>")
    return out

def make_preview_plane(line, out):
    row = ["<td>" + line[field] + "</td>" for field in DB_FIELDS[:7]]
    out.append("<tr>" + "".join(row) + "</tr>")
    return out
    
def make_preview_records(line, out):
    out.append("<tr><td>" + line + "</td></tr>")
    return out
    
################################################
    
def make_commit_flight(line, user, out):
    plane, created = Plane.objects.get_or_create(tailnumber=line.get("tailnumber"), type=line.get("type"), user=user)
    flight = Flight(user=request.user)
    line.update({"plane": plane.pk})
    form = ImportFlightForm(line, instance=flight)
    if form.is_valid():
        form.save()
        out.append("good: " + line.get('date') + "  " + line.get('remarks'))
    else:
        out.append(str(count) + "---------------------")
        out.append(" ".join(line))
        out.append(form.errors)
        out.append(str(count) + "---------------------")
        
    return out

#########################
       
def make_commit_nonflight(line, user, out):
    nf = NonFlight(user=user)
    form = NonFlightForm(line, instance=nf)

    if form.is_valid():
        form.save()
        out.append("good: " + line.get('date') + "  " + line.get('remarks'))
        
    else:
        out.append(str(count) + "---------------------")
        out.append(" ".join(line))
        out.append(form.errors)
        out.append(str(count) + "---------------------")
        
    return out
        
#########################
      
def make_commit_plane(line, user, out):
    tailnumber = line.get('tailnumber')
    manufacturer = line.get('manufacturer')
    model = line.get('model')
    type = line.get('type')
    cat_class = line.get('cat_class')
    rt = line.get('rt')
    tags = line.get('tags')
    
    p=Plane.objects.get(user=user, tailnumber=tailnumber, type=type)
    p.manufacturer=manufacturer
    p.model=model
    p.cat_class=cat_class
    p.tags=tags
    p.save()
    
    out.append("good: " + line.get('tailnumber'))
    
    return out

#########################
   
def make_commit_records(line, user, out):
    r,c=Records.objects.get_or_create(user=user)
    r.text=line.replace('\\r', '\n')
    r.save()
    
    out.append("good: " + line[:100])
    
    return out

#####################################################################################################

@login_required()
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
    
#####################################################################################################
    
def swap_out_flight_titles(original):
    new = []
    for title in original:
    
        title = title.upper().strip().replace("\"", '').replace(".", "")
    
        if title in COLUMN_NAMES.keys():
            new.append(COLUMN_NAMES[title])
        else:
            new.append("??")
            
    return new
    
#####################################################################################################

def swap_out_plane_titles(original):
    new = []
    for title in original:
    
        title = title.upper().strip().replace("\"", '').replace(".", "")
    
        if title in PLANE_COLUMN_NAMES.keys():
            new.append(PLANE_COLUMN_NAMES[title])
        else:
            new.append("??")
            
    return new
    














