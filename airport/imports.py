#!/srv/flightloggin/env/bin/python

import csv
import datetime
import os
import re
import sys

from psycopg2 import IntegrityError
from termcolor import colored




sys.path = ['/srv/', '/srv/flightloggin/'] + sys.path
from flightloggin import settings

from django.core.management import setup_environ
setup_environ(settings)


from django.conf import settings
PROJECT_PATH = settings.PROJECT_PATH
######################################################

from airport.models import Location, Region, Country, HistoricalIdent
from logbook.models import Flight
from route.models import RouteBase

from django.contrib.auth.models import User
ALL_USER = User(pk=1)

def latlng_match(old_lat, new_lat, old_lng, new_lng):
    """
    Returns true of the lat and long values are both the same from 8 decimal
    spaces
    """
    
    s = "%3.8f" # format both values to 8 decimal spaces to compare
    lng_match = s % float(old_lng) == s % float(new_lng)
    lat_match = s % float(old_lat) == s % float(new_lat)
    
    #return true if they both match
    return lat_match and lng_match

def re_render_all():
    for r in Route.objects.iterator():
        r.easy_render()

BANNED = ('46307', )   

def airports():   #import airport
    """
    id	 ident	type	name	latitude_deg	longitude_deg	elevation_ft	
    continent	iso_country	iso_region	municipality	scheduled_service
    gps_code	iata_code	local_code	home_link	wikipedia_link	keywords
    """
    
    path = os.path.join(PROJECT_PATH, 'airport', 'csv', 'airports.csv')
    f = open(path, 'rb')
    reader = csv.reader(f, "excel")
    titles = reader.next()
    reader = csv.DictReader(f, titles)

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

    # a list of idents that have changed, and therefore get HistoricalIdents
    hists = []

    for count, line in enumerate(reader):
        
        redo_after_save = False
        
        ##########################

        lat =    line["latitude_deg"]
        lng =    line["longitude_deg"]
        elev =   line["elevation_ft"]
        type_ =  line["type"]
        local =  line["local_code"]
        fback =  line['ident'].upper().replace('-', '')
        name =   line["name"].decode('utf-8')
        country= line["iso_country"].upper()
        city =   line["municipality"].decode('utf-8')
        region = line["iso_region"].upper()
        idd =    line['id']
        ident =  line['gps_code'].upper().replace('-', '')
        
        loc_wkt = "POINT ({0} {1})".format(float(lng), float(lat))
        
        if elev == "":
            elev = None

        if not ident or type_ == 'closed':
            # closed airports should use the ID ident, to avoid unique
            # name collisions
            ident = fback
            
        ##########################
                                           
        if country == "US":
            if (ident.startswith("K")
                and len(ident) == 4
                and re.search("[0-9]", ident)
               ):
                   
                # ourairports has a problem where non-icao identifiers in the
                # US are prefixed with a 'K' when they shouldn't be.
                
                ident = ident[1:] # remove the 'K'
                
            if (not ident.startswith("K")
                and len(ident) == 3
                and not re.search("[0-9]", ident)
                and not region == 'US-AK'):
                
                # there also is a problem where airports that should have
                # the 'K' do not
                   
                ident = "K" + ident
                
                
        if ident.startswith("US"):
            if local:
                ident = local

        ##########################
        
        if idd not in BANNED:
            l,c = Location.objects.get_or_create(pk=idd,
                                             user=ALL_USER,
                                             loc_class=1)
        else:
            l = Location(id=idd)
        
        if c:
            print "new airport:", ident
        
        elif idd in BANNED:
            print "BANNED: " + ident
            
        else:
            if not l.identifier == ident:
                a =  [colored(l.identifier, 'red'), colored(ident, 'green')]
                print u"changed ident!: {0} -> {1}".format(*a)
                hists.append(make_historical_ident(l, ident))
                redo_after_save = True
            
            elif not l.name == name:
                a = [ident, colored(l.name, 'red'), colored(name, 'green')]
                print u"changed name!:  {0} {1} -> {2}".format(*a)
                Flight.render_airport(ident)
            
            elif not l.municipality == city:
                a = [ident, colored(l.municipality, 'red'), colored(city, 'green')]
                print u"changed city!:  {0} {1} -> {2}".format(*a)
                Flight.render_airport(ident)
        
        l.municipality = city
        l.country = Country.objects.get(code=country)
        l.elevation = elev
        l.location = loc_wkt
        l.loc_type = types[type_]
        l.identifier = ident
        l.name = name
        l.region = Region.goon(code=region, country=country)
            
        try:
            if l.id not in BANNED:
                l.save()
            
            if redo_after_save:
                ## iff the ident has changed, we need to wait until the new
                ## location is saved before we re-render
                Flight.render_airport(ident)
                
            
        except Exception, e:
            print ident, e
            
        if (count % 500) == 0:
            #update user on status
            print colored("\n{0}\n".format(count), 'cyan')

    print "airports: {0}".format(count)
    print "hists:    {0}".format("\n".join([str(h) for h in hists if h]))
    
def make_historical_ident(l, new_ident):
    """
    Make an HistoricalIdent out of this airport because it's identifier is
    about to change.
    """
    
    used = RouteBase.objects.filter(location=l)[:1].count()
    print "used: " + str(used)

    if used > 0:
        msg = "Creating HistoricalIdent {0} -> {0}".format(l.identifier, new_ident)
        print colored(msg, 'yellow', attrs=['bold'])
        today = datetime.date.today()
        hi = HistoricalIdent(end=today, identifier=l.identifier, current_location=l)
        hi.save()
        return hi

###############################################################################

def navaids():
    """
    id	filename	ident	name	type	frequency_khz	latitude_deg	
    longitude_deg	elevation_ft	iso_country	dme_frequency_khz   dme_channel
    dme_latitude_deg	dme_longitude_deg	dme_elevation_ft
    slaved_variation_deg	magnetic_variation_deg	usageType	power
    associated_airport
    """
    
    path = os.path.join(PROJECT_PATH, 'airport', 'csv', 'navaids.csv')
    f = open(path, 'rb')
    
    reader = csv.reader(f, "excel")
    titles = reader.next()
    reader = csv.DictReader(f, titles)
    
    nav_types = {   '': 0,
                    'NDB': 9,
                    'NDB-DME': 10,
                    'VOR': 11,
                    'VORTAC': 12,
                    'TACAN': 13,
                    'VOR-DME': 14,
                    'DME': 15,
    }

    for count, line in enumerate(reader):
        
        ident = line["ident"]
        lat = line["latitude_deg"]
        lng = line["longitude_deg"]
        type_ = line["type"]
        name = line["name"]
        
        #to avoid collisions with airport pk's
        idd =  int(line['id']) + 100000 
        
        l,c = Location.objects.get_or_create(id=idd)
        
        # if the lat and lng values are the same, then skip the expensive
        # database process trying to figure out which region it belongs in
        skip_find_region = latlng_match(l.location.y, lat,
                                        l.location.x, lng)
        
        l.loc_class = 2
        l.identifier = ident
        l.name = name
        l.location = 'POINT (%s %s)' % (lng, lat)
        l.loc_type = nav_types[type_]
        l.user = ALL_USER
        
        if not skip_find_region:
            print "redoing region:", ident
            
        if c:
            print "new navaid:", ident
        
        try:
            l.save(skip_find_region=skip_find_region)
        except Exception, e:
            print "error:", ident, e
            
    print "navaids: {0}".format(count)

###############################################################################

def regions():   #import region
    """
    id	code	local_code	name	continent	iso_country	wikipedia_link
    keywords
    """

    path = os.path.join(PROJECT_PATH, 'airport', 'csv', 'regions.csv')
    f = open(path, 'rb')
    
    reader = csv.reader(f, "excel")
    titles = reader.next()
    reader = csv.DictReader(f, titles)

    for count, line in enumerate(reader):

        code = line["code"].upper()
        name = line["name"].decode('utf-8')
        country = line["iso_country"].upper()

        r,c = Region.objects.get_or_create(code=code)
        
        if name != r.name:
            a =  [colored(r.name, 'red'), colored(name, 'green')]
            print u"Changed region name!: {0} -> {1}".format(*a)
        
        r.name = name
        r.country = country
            
        if c:
            print "new region: " + code

    print "Regions: {0}".format(count)

###############################################################################

def countries():   #import country
    """
    id	code	name	continent	wikipedia_link	keywords
    """

    path = os.path.join(PROJECT_PATH, 'airport', 'csv', 'countries.csv')
    f = open(path, 'rb')
    
    reader = csv.reader(f, "excel")
    titles = reader.next()
    reader = csv.DictReader(f, titles)


    for count, line in enumerate(reader):

        code = line["code"].upper()
        name = line["name"].decode('utf-8')
        continent = line["continent"].upper()

        obj, c = Country.objects.get_or_create(code=code)
        
        if name != obj.name:
            a =  [colored(obj.name, 'red'), colored(name, 'green')]
            print u"Changed country name!: {0} -> {1}".format(*a)
        
        obj.continent = continent
        obj.name = name
        obj.save()
        
        if c:
            print "error: " + code

    print "Countries: {0}".format(count)


if __name__ == "__main__":
    start = datetime.datetime.now()
    
    countries()
    regions()
    airports()
    #navaids()
    
    print "total time: {0}".format(datetime.datetime.now() - start)

