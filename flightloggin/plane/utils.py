from django.db.models import Q
from django.db.models.query import QuerySet
from django.db.models import Sum
from flightloggin.main.mixins import UserMixin

class PlaneQuerySet(QuerySet, UserMixin):
    
    def user_common(self, u):
        """
        Filters the queryset by the passed user, as well as the 'common' user
        """
        from django.conf import settings
        return self.filter(user__in=(settings.COMMON_USER_ID, u.id) )
    
    def tailwheel(self):
        return self.filter( Q(tags__icontains="tailwheel"))
    
    def currency(self):
        """
        filters down to planes that are eligable for currency, e.g. tagged
        as either 'tr', 'type rating', or 'currency'
        """
        
        from django.db.models import Q

# bring this back when tagging registering works again
#
#        from tagging.models import TaggedItem, Tag       
#        curr_tags = Tag.objects.filter(
#                                        Q(name__iexact='type rating') |
#                                        Q(name__iexact='tr') |
#                                        Q(name__iexact='currency')
#                                      )
        
        return self.filter( Q(tags__icontains="type rating") |
                            Q(tags__contains="TR") |
                            Q(tags__icontains="currency")
                          )
