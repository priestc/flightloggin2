from django.contrib.sitemaps import Sitemap
from models import Location

class LocationSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.5

    def items(self):
        
        # exclude custom locations
        
        qs = Location.objects\
                     .exclude(loc_class=3)\
                     .values('identifier', 'loc_class')\
                     .order_by()\
                     .distinct()
        return qs
    
    def location(self, item):
        from django.core.urlresolvers import reverse
        if item.get('loc_class') == 1:
            view = "profile-airport"
            navaid = False
        else:
            view = "profile-navaid"
            navaid = True
            
        return reverse(view, kwargs={"ident": item.get('identifier')})

