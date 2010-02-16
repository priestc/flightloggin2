from django.contrib.gis.db.models.query import GeoQuerySet as QuerySet
from main.mixins import UserMixin

class RouteQuerySet(QuerySet, UserMixin):
    pass
