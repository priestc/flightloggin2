# Django settings for flightloggin project.

import os, sys
PROJECT_ROOT = os.path.abspath(os.path.join(__file__, '..', '..'))

ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)

MANAGERS = ADMINS

SECRET_KEY = 'sddjsdfjsdgfjhdgsjfhgdsjfhwnbcgsdjfbmenbfwjg'

ALLOWED_HOSTS = ['flightlogg.in', 'localhost:8000']

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'America/Chicago'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = False

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = False

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = ''

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = ''

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = os.path.join(PROJECT_ROOT, 'static')

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(PROJECT_ROOT, 'static_external'),
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    #'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'share.middleware.share.ShareMiddleware',
    'googlebot.middleware.LimitBotsMiddleware',
    'pipeline.middleware.MinifyHTMLMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'flightloggin.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'flightloggin.wsgi.application'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(PROJECT_ROOT, 'static_internal', 'templates'),
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'django.contrib.humanize',
    'django.contrib.gis',
    'django.contrib.sitemaps',
    # Uncomment the next line to enable admin documentation:
    # 'django.contrib.admindocs',

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
    'easydump',
    'style',
    #'etsy_colors',
    'landingpage',
    'badges',
    'twice_scroll',

    'raven.contrib.django',
    'tagging',
    'pagination',
    'gravatar',
    'django_openid_auth',
)

################

POSTGIS_TEMPLATE='template_postgis'

AUTH_PROFILE_MODULE = 'profile.Profile'

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.static',
    'django.core.context_processors.debug',
    'django.core.context_processors.request',
    'django.contrib.messages.context_processors.messages',
    'django.core.context_processors.media',
    'main.context_processors.user_label',
    'main.context_processors.proper_ad',
    'main.context_processors.old_browser',
    'main.context_processors.figure_navbar',
    'main.context_processors.site_url',
    'badges.context_processors.badge_count'
)

from django.template.loader import add_to_builtins
add_to_builtins('django.contrib.staticfiles.templatetags.staticfiles')

AUTHENTICATION_BACKENDS = (
    'django_openid_auth.auth.OpenIDBackend',
    'django.contrib.auth.backends.ModelBackend',
)

from settings_app import *
from settings_local import *
from settings_email import *

INSTALLED_APPS = INSTALLED_APPS + DEV_APPS

REGEX_USERNAME = "[\w\d.]{3,30}"
