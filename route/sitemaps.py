from django.contrib.sitemaps import Sitemap
from route.models import Route

class RouteSitemap(Sitemap):
    changefreq = "daily"
    priority = 0.5

    def items(self):
        return Route.objects\
                    .values_list('simple_rendered', flat=True)\
                    .order_by()\
                    .distinct()
    
    def location(self, item):
        from django.core.urlresolvers import reverse
        try:
            return reverse("profile-route", kwargs={"r": item})
        except:
            return ""
