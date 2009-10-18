from django.db.models import Q
from django.db.models.query import QuerySet
from django.db.models import Sum

class QuerySet(QuerySet):
    
    def user(self, u):
        return self.filter(user=u)
    
    def user_common(self, u):
        return self.filter(user__in=(1, u) )
