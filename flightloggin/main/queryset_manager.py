from django.contrib.gis.db.models import GeoManager
from django.db.models import Manager

class QuerySetMixin(object):
    def get_query_set(self):
        return self.model.QuerySet(self.model)
    
    def __getattr__(self, name):
        return getattr(self.get_query_set(), name)
    
class QuerySetManager(QuerySetMixin, Manager):
    pass

class GeoQuerySetManager(QuerySetMixin, GeoManager):
    pass
