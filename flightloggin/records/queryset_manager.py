from django.db.models.query import QuerySet
from main.mixins import UserMixin

class NonFlightQuerySet(QuerySet, UserMixin):
    pass
