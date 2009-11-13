import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'flightloggin.settings'
os.environ['MPLCONFIGDIR'] = '/var/cache/mpl'

import sys
sys.path = ['/srv/', '/srv/flightloggin/'] + sys.path

import site
from django.conf.settings import ENV_DIR
site.addsitedir(ENV_DIR + "/lib/python2.6/site-packages')

from django.core.handlers.wsgi import WSGIHandler
application = WSGIHandler()
