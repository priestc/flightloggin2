from django.db.models import Q
from django.db.models.query import QuerySet
from django.db.models import Sum

from main.mixins import UserMixin

class QuerySet(QuerySet, UserMixin):
    user_field = "flight__user"
