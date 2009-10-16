from datetime import datetime
import re
import csv

import settings
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse

from annoying.decorators import render_to
from annoying.functions import get_object_or_None

from share.decorator import no_share
from records.forms import NonFlightForm
from logbook.models import Flight
from records.models import Records, NonFlight
from plane.models import Plane

from logbook.constants import FIELD_TITLES
from constants import *
from forms import ImportForm, ImportFlightForm

@login_required()
@render_to('import.html')
@no_share
def import_s(request, shared, display_user):
    results={}
    preview = False
    
    if request.method == 'POST':
        if request.POST['submit'] == 'Import':
            preview = False
            preview_str=""
        elif request.POST['submit'] == 'Preview':
            preview = True
            preview_str="p"
            
        fileform = ImportForm(request.POST, request.FILES)
        
        if fileform.is_valid():
            filename = "%s/uploads/%s%s_%s.txt" % (settings.PROJECT_PATH,
                                                   request.user.username,
                                                   preview_str,
                                                   datetime.now())
            f = request.FILES['file']
            destination = open( filename , 'wb+')
            
            for chunk in f.chunks():
                destination.write(chunk)
            destination.close()
            
            results = do_import(request, f, preview=preview)

    else:
        fileform = ImportForm()
        
    display_user=request.user
    
    if preview:
        
        flight_header = "".join(
        ["<td>%s</td>" % FIELD_TITLES.get(title, "") for title in CSV_FIELDS]
        )
        
        flight_header = "<tr>%s</tr>" % flight_header
        
        plane_header = "".join(
                        ["<td>%s</td>" % title \
                            for title in \
                        ['Tailnumber',
                         'Manufacturer',
                         'Type',
                         'Model',
                         'Category/Class',
                         'TR',
                         'Tags']])
                         
        plane_header = "<tr>%s</tr>" % plane_header
        
        nonflight_header = "".join(
                        ["<td>%s</td>" % title \
                            for title in \
                        ['Date','Type','Remarks']])
                        
        nonflight_header = "<tr>%s</tr>" % nonflight_header
        
    loc=locals()    
    loc.update(results)
    return loc

###############################################################################

def do_import(request, f, preview=True):
    f.seek(0)
    pre = f.read(10000)
    f.seek(0)
    dialect = csv.Sniffer().sniff(pre)
    reader = csv.reader(f, dialect)
    titles = reader.next()
    titles = swap_out_flight_titles(titles)
    
    dr = csv.DictReader(f, titles, dialect=dialect)
    dr.next()
    
    non_out = []
    flight_out = []
    plane_out = []
    records_out = []
    
    del pre
    
    records=False
    
    for line in dr:
        
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
        
        if not line['date'] == "##PLANES":
            if preview:
                records_out = make_preview_records(line.get('date'),
                    records_out)
            else:
                records_out = make_commit_records(line.get('date'), 
                    request.user, records_out)
        
        try:
            header = dr.next()
            for line in dr:
                if preview:
                    plane_out = make_preview_plane(line, plane_out)
                else:
                    plane_out = make_commit_plane(line, request.user, plane_out)
        except StopIteration:   
            #most likley an empty planes section, just do nothing
            pass

            
    return {"flight_out": flight_out,
            "plane_out": plane_out,
            "non_out": non_out,
            "records_out": records_out}

###############################################################################

def prepare_line(line):
    
    if line.get('remarks', None):   
        line['remarks'] = line['remarks'].replace('\\r', '\n')
    
    if line.get('non_flying'):
        return "NON-FLIGHT", line
        
    if line.get('date', [])[:12] == "##RECORDS":
        return "RECORDS", line
        
    if line.get('date', [])[:11] == "##PLANES":
        return "PLANE", line
        
    instructor = line.get('instructor', "")
    student = line.get('student', "")
    captain = line.get('captain', "")
    fo = line.get('fo', "")
    
    if line.get("simulator") and not line.get("total"):
        line['total'] = line.get("simulator")
        
    if line.get('to') and line.get('from') and not line.get('via'):
        line.update({"route": "%s %s" % (line.get('from'), line.get('to'))})
        
    elif line.get('to') and line.get('from') and line.get('via'):
        line.update({
        "route": "%s %s %s" % (
        line.get('from'), line.get('via'), line.get('to'))
        })
        
    if line.get('holding', "").upper() == "NO":
        line['holding'] = False
        
    if line.get('tracking', "").upper() == "NO":
        line['tracking'] = False
    
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
    else:
        l = [instructor, fo, captain, student]

    for x in l:
        if x:
            person = x
            break
    
    if person:
       line.update({"person": person})

    return "FLIGHT", line

##### each of these functions returns an html table row #######################

def make_preview_flight(line, out):
    row = ["<td>%s</td>" % line.get(field, "") for field in CSV_FIELDS]
    out.append("<tr>" + "".join(row) + "</tr>")
    return out
    
def make_preview_nonflight(line, out):
    row = ["<td>%s</td>" % line.get('date'),
           "<td>%s</td>" % NON_FLIGHT_TRANSLATE_TEXT[line.get('non_flying')],
           "<td>%s</td>" % line.get('remarks'),
          ]
    out.append("<tr>" + "".join(row) + "</tr>")
    return out

def make_preview_plane(line, out):
    row = []
    for field in CSV_FIELDS[:7]:
        row.append("<td>%s</td>" % line.get(field, ""))
        
    out.append("<tr>" + "".join(row) + "</tr>")
    return out
    
def make_preview_records(line, out):
    out.append("<tr><td colspan='20'>" + line + "</td></tr>")
    return out
    
################################################
    
def make_commit_flight(line, user, out):
    kwargs = {"tailnumber":line.get("tailnumber"), "user": user}
    if line.get("type"):
        kwargs.update({"type": line.get("type")})
        
    plane, created = Plane.objects.get_or_create(**kwargs)

    flight = Flight(user=user)
   
    ## must be "ff", instead of "" because it must be iterable, "" is not
    ## iterable
    
    if "P" in (line.get("flying", "fff") or "ff"):
        line.update({"pilot_checkride": True})
    
    if "H" in (line.get("flying", "fff") or "ff"):
        line.update({"holding": True})
        
    if "T" in (line.get("flying", "fff") or "ff"):
        line.update({"tracking": True})
        
    if "C" in (line.get("flying", "fff") or "ff"):
        line.update({"cfi_checkride": True})
        
    if "I" in (line.get("flying", "fff") or "ff"):
        line.update({"ipc": True})
          
    line.update({"plane": plane.pk})
    form = ImportFlightForm(line, instance=flight)
    

    if form.is_valid():
        form.save()
        out.append("<tr><td>good</td><td>%s</td><td>%s</td></tr>" %
                        (str(line.get('date')), str(line.get('remarks'))))
    else:
        out.append("<tr class='bad'><td>")
        out.append("</td><td>".join([str(v) for v in line.values()]))
        out.append("</td><tr class='bad'><td colspan=21>")
        out.append(form.errors)
        out.append("</td></tr>")
        
    return out

#########################
       
def make_commit_nonflight(line, user, out):
    
    nf = NonFlight(user=user)
    new_nf = NON_FLIGHT_TRANSLATE_NUM[line.get('non_flying', "")]
    line.update({'non_flying': new_nf})
    form = NonFlightForm(line, instance=nf)

    if form.is_valid():
        form.save()
        out.append("<tr><td>good</td><td>%s</td><td>%s</td></tr>" %
                (line.get('date'), line.get('remarks')))
        
    else:
        out.append("<tr class='bad'><td>")
        out.append("<tr class='bad'><td>bad:</td><td>%s</td><td>%s</td></tr>" %
                (line.get('date'), line.get('remarks')))
        out.append("</td><tr class='bad'><td colspan=5>")
        out.append(form.errors)
        out.append("</td></tr>")
        
    return out
        
#########################
      
def make_commit_plane(line, user, out):
    tailnumber = line.get('date')
    manufacturer = line.get('tailnumber')
    model = line.get('type')
    type_ = line.get('route')
    cat_class = line.get('total')
    rt = line.get('pic')
    tags = line.get('solo')
    
    p,c=Plane.objects.get_or_create(user=user, tailnumber=tailnumber, type=type_)
    p.manufacturer=manufacturer
    p.model=model
    p.cat_class=cat_class
    
    the_tags = []
    if tags:
        for tag in tags.split(","):
            tag = tag.strip()
            if tag.find(" ") > 0:
                tag = "\"" + tag + "\""
                
            the_tags.append(tag)
    
    p.tags = " ".join(the_tags)
    p.save()
    
    out.append("<tr><td>good</td><td>" + line.get('tailnumber') + "</td></tr>")
    
    return out

#########################
   
def make_commit_records(line, user, out):
    r,c=Records.objects.get_or_create(user=user)
    r.text=line.replace('\\r', '\n')
    r.save()
    
    out.append("good: " + line[:100])
    
    return out

###############################################################################
    
def swap_out_flight_titles(original):
    new = []
    for title in original:
        # replace /n and /r because of logbook pro
        title = title.upper().strip().replace("\"", '').replace(".", "").\
                replace("\r\n", " ")
        if title in COLUMN_NAMES.keys():
            new.append(COLUMN_NAMES[title])
        else:
            new.append(title)
            
    return new
    
###############################################################################

def swap_out_plane_titles(original):
    new = []
    for title in original:
    
        title = title.upper().strip().replace("\"", '').replace(".", "")
    
        if title in PLANE_COLUMN_NAMES.keys():
            new.append(PLANE_COLUMN_NAMES[title])
        else:
            new.append("??")
            
    return new
    














