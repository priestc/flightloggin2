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
        path = os.path.join(settings.PROJECT_ROOT, 'airport', 'csv', 'countries.csv')
        if options['download']:
            os.system('wget http://www.ourairports.com/data/countries.csv -O %s' % path)

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
                print "new country!: " + code

        print "Countries: {0}".format(count)
        