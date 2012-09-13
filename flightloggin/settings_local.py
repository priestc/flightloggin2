DEBUG = False
TEMPLATE_DEBUG = DEBUG

from settings_private import *

DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'logbook',                      # Or path to database file if using sqlite3.
        'USER': 'ubuntu',                      # Not used with sqlite3.
        'PASSWORD': 'spatula',                  # Not used with sqlite3.
        'HOST': 'flightlogg.in',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}

#the url title where the states will show up, eg: http://flightlogg.in/states/user would be 'states'
STATES_URL = 'states'

## the user id of the demo user
DEMO_USER_ID = 2
UNKNOWN_PLANE_ID = 90
COMMON_USER_ID = 1

DEV_APPS = ('django_extensions', )

from settings_logger import *
from settings_email import *
