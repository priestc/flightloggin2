from django.contrib.gis.db.models.query import GeoQuerySet
from main.mixins import UserMixin

class RouteQuerySet(GeoQuerySet, UserMixin):
    pass
