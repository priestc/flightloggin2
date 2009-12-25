from django.contrib.sitemaps import Sitemap
from models import Location

class LocationSitemap(Sitemap):
    changefreq = "daily"
    priority = 0.5

    def items(self):
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
            
        return reverse(view, kwargs={"pk": item.get('identifier')})

