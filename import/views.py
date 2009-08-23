from datetime import datetime
import re
import csv

import settings
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect

from annoying.decorators import render_to
from annoying.functions import get_object_or_None

from logbook.forms import NonFlightForm
from logbook.models import NonFlight, Flight
from records.models import Records

from logbook.constants import FIELD_TITLES
from constants import *
from forms import ImportForm, ImportFlightForm

@render_to('import.html')
def do_import(request, f, preview=True):

    reader = csv.reader(f, delimiter='\t')
    titles = reader.next()
    
    your_header = "<tr>" + "".join(["<td>" + title + "</td>" for title in titles])
    
    titles = swap_out_flight_titles(titles)
    
    official_header = "<tr>" + "".join(["<td>" + FIELD_TITLES.get(title, "") + "</td>" for title in titles])
    
    dr = csv.DictReader(f, titles, delimiter='\t')
    dr.next()
    
    non_out = []
    flight_out = []
    plane_out = []
    records_out = []
    
    records=False
    count = 0
    
    for line in dr:
        count += 1
        
        line_type, dict_line = prepare_line(line)

        if line_type == "FLIGHT":
            if preview:
                flight_out = make_preview_flight(dict_line, flight_out)
            else:
                flight_out = make_commit_flight(dict_line, request.user, flight_out)

        elif line_type == "NON-FLIGHT":
            if preview:
                non_out = make_preview_nonflight(dict_line, non_out)
            else:
                non_out = make_commit_nonflight(dict_line, request.user, non_out)
                
        elif line_type == "RECORDS":
            records = True
            break
     
    if records:
        line = dr.next()
        print "records " + str(count)
        
        if preview:
            records_out = make_preview_records(line.get('date'), records_out)
        else:
            records_out = make_commit_records(line.get('date'), request.user, records_out)
            
        header = dr.next()
        line = dr.next()
        count += 1
        
        for line in dr:
            count += 1
            if preview:
                plane_out = make_preview_plane(line, plane_out)
            else:
                plane_out = make_commit_plane(line, request.user, plane_out)
            
    return {"your_header": your_header, "official_header": official_header, "flight_out": flight_out, "plane_out": plane_out, "non_out": non_out, "records_out": records_out}

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
    
    if line.get("simulator") and not line.get("total"):
        line['total'] = line.get("simulator")
    
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
    row = ["<td>" + line.get(field, "") + "</td>" for field in CSV_FIELDS]
    out.append("<tr>" + "".join(row) + "</tr>")
    return out
    
def make_preview_nonflight(line, out):
    row = ["<td>" + line.get('date', "") + "</td>",
           "<td>" + NON_FLIGHT_TRANSLATE_TEXT[line.get('non_flying', "")] + "</td>",
           "<td>" + line.get('remarks', "") + "</td>",
          ]
    out.append("<tr colspan='20'>" + "".join(row) + "</tr>")
    return out

def make_preview_plane(line, out):
    row = []
    for field in CSV_FIELDS[:7]:
        row.append("<td>" + line.get(field, "") + "</td>")
        
    out.append("<tr>" + "".join(row) + "</tr>")
    return out
    
def make_preview_records(line, out):
    out.append("<tr><td colspan='20'>" + line + "</td></tr>")
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
    














