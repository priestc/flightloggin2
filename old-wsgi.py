import sys
sys.path = ['/srv/', '/srv/flightloggin/'] + sys.path

import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'flightloggin.settings'
os.environ['MPLCONFIGDIR'] = '/var/cache/mpl'
os.environ["CELERY_LOADER"] = "django"

from site import addsitedir
from local_settings import ENV_DIR
addsitedir(ENV_DIR + "/lib/python2.7/site-packages")

from django.core.handlers.wsgi import WSGIHandler
application = WSGIHandler()
