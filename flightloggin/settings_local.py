DEBUG = False
DEBUG_TOOLBAR = False

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'dongs'

DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': 'logbook',
        'USER': 'chris',                  # Not used with sqlite3.
        'PASSWORD': 'spatula',         # Not used with sqlite3.
        'HOST': 'localhost',                    # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}

RECAPTCHA_PRIVATE_KEY = '6LeOlLoSAAAAAAmlpMTXJHN0i_vpDOxekaDPrEoU'

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = '/srv/flightloggin/media'

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = '/fl-media'
SITE_URL = "http://flightlogg.in"

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/ad-media/'

SERVER_EMAIL = 'info@fanmarkers.com'
EMAIL_HOST = "localhost"
EMAIL_HOST_PASSWORD = ""
EMAIL_HOST_USER = ""
EMAIL_PORT = 25
DEFAULT_FROM_EMAIL = "info@flightlogg.in"

POSTGIS_TEMPLATE='template_postgis'

ENV_DIR = '/srv/flightloggin/.fl_env'
UPLOADS_DIR = '/var/fl-uploads'

#the path where the state maps are stored
BASE_MAP_PATH = '/var/www/states'

#CACHE_BACKEND = 'db://logbook_cache'
#CACHE_BACKEND = 'file:///var/tmp/django_cache'
#CACHE_BACKEND = 'memcached://127.0.0.1:11211/'
#CACHE_BACKEND = 'main.pylibmcd://127.0.0.1:11000/'

#the url title where the states will show up, eg: http://flightlogg.in/states/user would be 'states'
STATES_URL = 'states'

## the user id of the demo user
DEMO_USER_ID = 2
UNKNOWN_PLANE_ID = 90
COMMON_USER_ID = 1

FACEBOOK_API_KEY = '8d04d4c1a5fae94c84b4a80b6f335cff'
FACEBOOK_SECRET_KEY = '371872497b3372e740aed99c83fd2d7e'

# for Amazon S3
AWS_ACCESS_KEY = 'AKIAJDBRZGUZ2PE334MQ'
AWS_SECRET_KEY = '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'


GOOGLE_MAPS_KEY = "ABQIAAAAtDznsRv92g_KZ0HK9mBD5RS3ydai3R5pSwWU_IHTQxn79Z9awhQaWXs60I2yGfPRz5z-Bs_CTn5lMg"

INSTALLED_APPS = ['django_extensions', ]