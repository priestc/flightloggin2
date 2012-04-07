import os

from django.conf import settings

PROJECT_ROOT = getattr(settings, 'PROJECT_ROOT', None)
TEMP_LOCATION = getattr(settings, 'TEMP_LOCATION', None)

# these attrs are added to each manifest (user's prefs override)
MANIFEST_DEFAULTS = {
    'jobs': 8,
    'save_path': '.'
}

class DumpMixin(object):
    """
    Common methods for all dump commands
    """
    
    def get_manifest(self, name):
        """
        Given a dump name, get the manifest and the credentials for that dump
        from settings.DATABASES
        """
        # get manifest from settings
        DUMP_MANIFEST = getattr(settings, 'DUMP_MANIFEST')
        raw_manifest = DUMP_MANIFEST[name]
        
        # apply defaults
        MANIFEST_DEFAULTS.update(raw_manifest)
        manifest = MANIFEST_DEFAULTS
        
        # replace database key with settings from DATABASES setting
        manifest['database'] = settings.DATABASES[manifest['database']]
        
        # sanity checks
        engine = manifest['database']['ENGINE']
        assert 'postgis' in engine, "Sorry, only postgres/postgis supported"
        
        # determine where the dump should be saved
        path = self.get_save_path()
        save_path = os.path.join(path, '{0}-{{key}}'.format(name))
        manifest['save_path'] = save_path
        
        return manifest
        
    def get_save_path(self):
        """
        Based on the settings provided, figure out where to save/get incoming
        dumps.
        """
        if TEMP_LOCATION:
            return TEMP_LOCATION

        if PROJECT_ROOT:
            return PROJECT_ROOT

        return '.' # if no setting can be found, use current dir