from optparse import make_option

from django.core.management.base import NoArgsCommand
from django.conf import settings

import datetime
import csv
import os
import sys
import re

from warnings import warn

from airport.models import Region, Country
from airport.imports import airports as update_airports

CSV_LOCATION = os.path.join(settings.PROJECT_ROOT, 'airport', 'csv')

types = {
   '': 0,
   'balloonport': 7,
   'closed': 4,
   'heliport': 5,
   'large_airport': 3,
   'medium_airport': 2,
   'seaplane_base': 6,
   'small_airport': 1,
}

def clean_line(line):
    global REGIONS
    
    lat =    line["latitude_deg"]
    lng =    line["longitude_deg"]
    elev =   line["elevation_ft"]
    type_ =  line["type"]
    local =  line["local_code"]
    fback =  line['ident'].upper()
    name =   line["name"].decode('utf-8')
    country= line["iso_country"].upper()
    city =   line["municipality"].decode('utf-8')
    region = line["iso_region"].upper()
    idd =    line['id']
    ident =  line['gps_code'].upper()
    iata =   line['iata_code']
    icao =   ""
    local =  ""
    
    ## construct new variables
    
    point = "POINT ({0} {1})".format(float(lng), float(lat))
    region_id = REGIONS[region]
    airport_type = types[type_]    
    
    if not ident or type_ == 'closed':
        # closed airports should use the ID ident, to avoid unique
        # name collisions
        ident = fback
    
    numeric = re.search("[0-9]", ident)
    
    ######## construct icao
    
    if len(ident) == 4 and not numeric:
        icao = ident
        local = ""
        
    ####### construct iata
    
    if not iata and icao and country == 'US':
        iata = icao[1:]
        local = ""
        
    ##### fix ourairpots messed up data
        
    if '-' in ident:
        no_local = True
        ident = ident.replace('-', '')
    else:
        no_local = False
       
    if country == "US":
        if (ident.startswith("K")
            and len(ident) == 4
            and numeric
           ):
            
            ## in the format: K95F
            
            # ourairports has a problem where non-icao identifiers in the
            # US are incorrectly prefixed with a 'K' when they shouldn't be.
            
            ident = ident[1:] # remove the 'K'
            local = ident
            icao = ''
            iata = ''
            
        if (not ident.startswith("K")
            and len(ident) == 3
            and not numeric
            and not region == 'US-AK'):
            
            ## in the format: HIU
            
            # there also is a problem where airports that should have
            # the 'K' do not
               
            ident = "K" + ident
            icao = ident
        
        if not icao and not iata:
            local = ident   
            
        if ident.startswith("US"):
            if local:
                ident = local
                
        if iata == '' and icao.startswith('K'):
            iata = icao[1:]

    if country == 'CA':
        if numeric:
            local = ident

    if numeric:
        # any airport with a numeric identifier has neither
        # an iata nor icao code
        icao = ""
        iata = ""
        
    if no_local:
        ## the identifier is a "US-0041" format identifier,
        ## which is not an official local identifier for any country
        local = ''

    if len(ident) == 4 and not numeric:
        ## no matter what, any identifier thats 4 letters
        ## and fully alpha, it is an icao identifier
        icao = ident
    
    if local == icao:
        ## local and ident are never the same
        local = ""
    
    ############# return new line #################################
    
    numeric = re.search("[0-9]", ident)
    
    if icao and (not len(icao) == 4 or re.search("[0-9]", icao)):
        warn("Incorrect ICAO: %s" % icao)
    if iata and (not len(iata) == 3 or re.search("[0-9]", iata)):
        warn("Incorrect IATA: %s" % iata)
    if local and not len(local) in (3,4):
        warn("Incorrect Local: %s" % local)
    
    return [
        int(idd),
        ident,
        icao,
        iata,
        local,
        name.encode('utf-8'),
        city.encode('utf-8'),
        point,
        airport_type,
        country,
        int(region_id),
        elev
    ]


class Command(NoArgsCommand):
    help = 'Sends email backups to each user depending on their preferences'
    
    option_list = NoArgsCommand.option_list + (
        make_option(
            '--download',
            '-d',
            dest='download',
            action='store_true',
            help="Download the latest csv from OurAirports",
        ),
    )
    
    def handle(self, *args, **options):
        start = datetime.datetime.now()
        global REGIONS
        
        REGIONS = {}
        for d in Region.objects.values('code', 'pk'):
            REGIONS.update({d['code']: d['pk']})

        old = open(os.path.join(CSV_LOCATION, "airports.csv"), 'rb')
        new = open(os.path.join(CSV_LOCATION, "airports_new.csv"), 'w')

        reader = csv.reader(old, "excel")
        titles = reader.next()
        reader = csv.DictReader(old, titles)
        writer = csv.writer(new, delimiter=",")

        new = []
        print "Generating... ",
        for n,line in enumerate(reader):
            new.append(clean_line(line))
        print "Done"

        # sort by master ident
        print "Sorting... ",
        sys.stdout.flush()
        rows_sorted = sorted(new, key=lambda x: x[1])
        print "Done"

        print "Writing... ",
        sys.stdout.flush()
        ## make header
        writer.writerow(['id', 'ident', 'icao', 'iata', 'local',
                         'name', 'city', 'point', 'type', 'country',
                         'region', 'elev'])
        for row in rows_sorted:
            writer.writerow(row)
        print "Done"
        print "total parsing/rwriting execution time: {0}".format(datetime.datetime.now() - start)
        
        update_airports()
        