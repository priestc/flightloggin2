import os
import sys

sys.path = ['/srv', '/srv/flightloggin'] + sys.path
os.environ['DJANGO_SETTINGS_MODULE'] = 'flightloggin.settings'

from django.core.handlers.wsgi import WSGIHandler
application = WSGIHandler()
