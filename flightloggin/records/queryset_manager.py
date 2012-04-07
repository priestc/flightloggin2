from django.db.models.query import QuerySet
from flightloggin.main.mixins import UserMixin

class NonFlightQuerySet(QuerySet, UserMixin):
    pass
