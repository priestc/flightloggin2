# easydump settings ##############################

EASYDUMP_MANIFESTS = {
    'default': {
        'database': 'default',
        'exclude-models': ('WorldBorders', 'USStates'),
        's3-bucket': 'fl_dumps'
    },
    'geographical': {
        'database': 'default',
        'include-models': ('WorldBorders', 'USStates'),
        's3-bucket': 'fl_dumps'
    }
}

# openid settings ################################

OPENID_CREATE_USERS = True
OPENID_UPDATE_DETAILS_FROM_SREG = True
LOGIN_URL = "/openid/login/"
LOGIN_REDIRECT_URL = '/'

# debug bar settings #############################

INTERNAL_IPS = ('127.0.0.1','192.168.1.145')
DEBUG_TOOLBAR_CONFIG = {"INTERCEPT_REDIRECTS": False}

########### flightloggin settings

ENV_DIR = '/srv/flightloggin/.fl_env'
UPLOADS_DIR = '/var/fl-uploads'

#the path where the state maps are stored
BASE_MAP_PATH = '/var/www/states'

EASYDUMP_MANIFESTS = {
    'default': {
        'database': 'default',
        's3-bucket': 'fl_dumps',
    }
}

BADGES_ENABLE = True

PIPELINE_CSS = {
    'logbook': {
        'source_filenames': (
          'logbook.sass',
          'fancy_route.sass',
          'filter_table.sass',
          'flight_popup.sass',
        ),
        'output_filename': 'logbook.css',
        'extra_context': {
            'media': 'screen,projection',
        },
    },
    'site_stats': {
        'source_filenames': (
            'site_stats.sass',
        ),
        'output_filename': 'site_stats.css',
    },
}

PIPELINE_JS = {
    'logbook': {
        'source_filenames': (
          'js/logbook.js',
          'js/sprintf.js',
          'js/popup.js',
          'js/flight_popup.js',
        ),
        'output_filename': 'js/logbook.js',
    }
}

PIPELINE_COMPILERS = (
  'pipeline.compilers.sass.SASSCompiler',
)

PIPELINE_SASS_BINARY = '/usr/bin/sass'
