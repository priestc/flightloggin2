SERVER_EMAIL = 'info@fanmarkers.com'
EMAIL_HOST = "localhost"
EMAIL_HOST_PASSWORD = ""
EMAIL_HOST_USER = ""
EMAIL_PORT = 25
DEFAULT_FROM_EMAIL = "info@flightlogg.in"

DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'logbook',                      # Or path to database file if using sqlite3.
        'USER': 'chris',                      # Not used with sqlite3.
        'PASSWORD': 'spatula',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
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

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}