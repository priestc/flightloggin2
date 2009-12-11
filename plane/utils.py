from django.db.models import Q
from django.db.models.query import QuerySet
from django.db.models import Sum
from main.mixins import UserMixin

class PlaneQuerySet(QuerySet, UserMixin):
    
    def user_common(self, u):
        return self.filter(user__in=(1, u.id) )
    
    def currency(self):
        """ filters down to planes that are eligable for currency, e.g. tagged
            as either 'tr', 'type rating', or 'currency'
        """
        
        from django.db.models import Q
        
        return self.filter( Q(tags__icontains="type rating") |
                            Q(tags__icontains="tr") |
                            Q(tags__icontains="currency")
                          )
