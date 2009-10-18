#! /usr/bin/env python
import os, sys
import csv, re
from psycopg2 import IntegrityError
from airport.models import Location, Region, Country
from django.contrib.gis.geos import Point

project_name = sys.argv[1]

THIS_PATH = "/home/chris/Websites/" + project_name + "/airport/fixtures/"

#######################################################################

def main():
    print "Importing Countries..."
    countries()

    print "Importing Regions..."
    regions()
    
    print "Importing Airports..."
    airports()
    
    if project_name == "flightloggin": 
        print "Importing Navaids..."
        navaids()
    
#######################################################################

def airports():   #import airport
    """
    id	 ident	type	name	latitude_deg	longitude_deg	elevation_ft	
    continent	iso_country	iso_region	municipality	scheduled_service
    gps_code	iata_code	local_code	home_link	wikipedia_link	keywords
    """
    path = os.path.join(THIS_PATH, 'airports.csv')
    f = open(path, 'rb')
    reader = csv.reader(f, "excel")
    titles = reader.next()
    reader = csv.DictReader(f, titles)

    count=0
    count2=0
    count_to = 0

    types = {       '': 0,
                    'balloonport': 7,
                    'closed': 4,
                    'heliport': 5,
                    'large_airport': 3,
                    'medium_airport': 2,
                    'seaplane_base': 6,
                    'small_airport': 1,
            }

    for line in reader:

        throw_out = False
        count += 1
        
        #if count > 30:
        #    break
        
        ##########################

        lat =    line["latitude_deg"]
        lng =    line["longitude_deg"]
        elev =   line["elevation_ft"]
        type_ =  line["type"]
        local =  line["local_code"]
        ident =  line['ident'].upper()
        name =   line["name"]
        country= line["iso_country"].upper()
        city =   line["municipality"]
        region = line["iso_region"].upper()
        
        if elev == "":
            elev=None

        ##########################

        if ident[:2].upper() == "X-":           ## throw out all closed airports with "X" identifiers
            throw_out = True

        if country == "US":                                     ## US AIRPORTS
            if ident[0] == "K":                             ## STARTS WITH K
                if re.search("[0-9]", ident):           ## HAS NUMBER
                    ident = ident[1:]               ## get rid of the K

        if ident[:3] == "US-":
            if local:
                ident = local
            else:
                ident = ident[3:]                       ## get rid of the "US-" part


        if not throw_out:

            try:
                p, created = Location.objects.get_or_create(
                    loc_class=     1,
                    identifier=    ident,
                    name=          name,
                    region=        Region.goon(code=region, country=country),
                    municipality=  city,
                    country=       Country.objects.get(code=country),
                    elevation=     elev,
                    location=      Point(float(lng), float(lat)),
                    loc_type=      types[type_]
                )
                
                count2 += 1
                
                if not created:
                    print "already - " + ident

            except ValueError:
                print "value - " + ident

            except IntegrityError:
                print "integrity - " + ident
            
            except TypeError:
                print "type - " + ident
                
            

        else:
            count_to += 1

    print "total:      " + str(count)
    print "success:    " + str(count2)
    print "thrown out: " + str(count_to)

######################################################################################

def regions():   #import region
    """
    id	code	local_code	name	continent	iso_country	wikipedia_link	keywords
    """

    path = os.path.join(THIS_PATH, 'regions.csv')
    f = open(path, 'rb')
    reader = csv.reader(f, "excel")
    titles = reader.next()
    reader = csv.DictReader(f, titles)
    count=0

    for line in reader:
        count += 1

        code = line["code"].upper()
        name = line["name"]
        country = line["iso_country"].upper()

        try:
            Region.objects.get_or_create(name=name, code=code, country=country, )
        except:
            print code

    print "total lines: " + str(count)

######################################################################################

def countries():   #import country
    """
    id	code	name	continent	wikipedia_link	keywords
    """

    path = os.path.join(THIS_PATH, 'countries.csv')
    f = open(path, 'rb')
    reader = csv.reader(f, "excel")
    titles = reader.next()
    reader = csv.DictReader(f, titles)

    count=0

    for line in reader:

        count += 1

        ##########################

        code = line["code"].upper()
        name = line["name"]
        continent = line["continent"].upper()

        try:
            Country.objects.get_or_create(name=name, code=code, continent=continent)
        except:
            print "error: " + code

    print "lines: " + str(count)
    
######################################################################################
def navaids():
    """
    id	filename	ident	name	type	frequency_khz	latitude_deg	
    longitude_deg	elevation_ft	iso_country	dme_frequency_khz   dme_channel
    dme_latitude_deg	dme_longitude_deg	dme_elevation_ft
    slaved_variation_deg	magnetic_variation_deg	usageType	power
    associated_airport
    """
    THIS_PATH = "/home/chris/Websites/flightloggin/airport/fixtures/"
    path = os.path.join(THIS_PATH, 'navaids.csv')
    f = open(path, 'rb')
    reader = csv.reader(f, "excel")
    titles = reader.next()
    reader = csv.DictReader(f, titles)

    count=0
    
    nav_types = {   '': 0,
                    'NDB': 9,
                    'NDB-DME': 10,
                    'VOR': 11,
                    'VORTAC': 12,
                    'TACAN': 13,
                    'VOR-DME': 14,
                    'DME': 15,
    }

    for line in reader:
        count += 1
        #if count > 30:
        #    break
        
        ident = line["ident"]
        lat = line["latitude_deg"]
        lng = line["longitude_deg"]
        type = line["type"]
        name = line["name"]
        
        kwargs = {"loc_class":     2,
                  "identifier":    ident,
                  "name":          name,
                  "location":      'POINT (%s %s)' % (lng, lat),
                  "loc_type":      nav_types[type],
                 }
        
        try:
            navaid, created = Location.objects.get_or_create(**kwargs)
            
            if not created:
                print "already - %s" % ident

        except ValueError:
            print "value - %s" % ident

        except IntegrityError:
            print "integrity - %s" % ident
        
        except TypeError:
            print "type - %s" % ident
            
        except:
            import pdb; pdb.set_trace()
            print "total fail - %s" % ident
        
        
######################################################################################
######################################################################################

if __name__ == "__main__":
    main()

