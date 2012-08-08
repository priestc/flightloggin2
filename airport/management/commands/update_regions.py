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
from termcolor import colored

class Command(NoArgsCommand):
    help = 'Update the Region database'
    
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
        path = os.path.join(settings.PROJECT_ROOT, 'airport', 'csv', 'regions.csv')
        if options['download']:
            os.system('wget http://www.ourairports.com/data/regions.csv -O %s' % path)
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

            r.save()

            if c:
                print "new region: " + code

        print "Regions: {0}".format(count)