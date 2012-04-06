import os, sys
from local_settings import *

PROJECT_PATH = os.path.abspath(os.path.dirname(__file__))
TEMPLATE_DEBUG = DEBUG

AUTH_PROFILE_MODULE = 'profile.profile'

GOOGLE_ANALYTICS_CODE = "UA-501381-5"

## gravatar settings
GRAVATAR_DEFAULT_IMAGE = "http://flightlogg.in/fl-media/images/empty.png"

## postgis setting for testing
TEST_RUNNER='django.contrib.gis.tests.run_tests'

# forum new style settings
FORUM_USE_RECAPTCHA = True
RECAPTCHA_PUBLIC_KEY = '6LeOlLoSAAAAAIQyHuTVkL0gRmY0A36igAExm7le'
FORUM_OVERALL_NAME = "The FlightLogg.in' Forums"

# debug bar settings#############################
INTERNAL_IPS = ('127.0.0.1','192.168.1.145')
DEBUG_TOOLBAR_CONFIG = {"INTERCEPT_REDIRECTS": False}

#openid settings #################################

OPENID_CREATE_USERS = True
OPENID_UPDATE_DETAILS_FROM_SREG = True
LOGIN_URL = "/openid/login/"
LOGIN_REDIRECT_URL = '/'

AUTHENTICATION_BACKENDS = (
    'django_openid_auth.auth.OpenIDBackend',
    'django.contrib.auth.backends.ModelBackend',
)

###################################################

ADMINS = (
    ("Chris Priest", "nbvfour@gmail.com"),
)

MANAGERS = ADMINS

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'America/New_York'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = False

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
#     'django.template.loaders.eggs.load_template_source',
)

MIDDLEWARE_CLASSES = [
    'facebook.djangofb.FacebookMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'pagination.middleware.PaginationMiddleware',
    'share.middleware.share.ShareMiddleware',
    'googlebot.middleware.LimitBotsMiddleware',
]

if DEBUG_TOOLBAR:
    MIDDLEWARE_CLASSES += ['debug_toolbar.middleware.DebugToolbarMiddleware', ]

ROOT_URLCONF = 'flightloggin.urls'

TEMPLATE_DIRS = (
    os.path.join(PROJECT_PATH, 'templates')
)

INSTALLED_APPS += [
    'logbook',
    'records',
    'plane',
    'airport',
    'main',
    'profile',
    'route',
    'site_stats',
    'realtime',
    'backup',
    'maps',
    'realtime',
    'graphs',
    'currency',
    'auto8710',
    'sigs',
    'milestones',
    'manage',
    'facebook_app',
    'easydump',
    
    'tagging',
    'pagination',
    'gravatar',
    'django_openid_auth',
    
    'django.contrib.admin',
    'django.contrib.admindocs',
    'django.contrib.auth',
    'django.contrib.humanize',
    'django.contrib.contenttypes',
    'django.contrib.gis',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.sitemaps',
]

if DEBUG_TOOLBAR:
    INSTALLED_APPS += ['debug_toolbar', ]

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.request',
    'django.core.context_processors.media',
    'main.context_processors.user_label',
    'main.context_processors.proper_ad',
    'main.context_processors.old_browser',
    'main.context_processors.figure_navbar',
    'main.context_processors.site_url',
)

DUMP_MANIFEST = {
    'default': {
        'database': 'default',
        'exclude-models': 'Location',
        's3-bucket': 'fl_dumps'
    }
}
