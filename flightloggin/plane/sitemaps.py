from django.contrib.sitemaps import Sitemap
from models import Plane

class TailnumberSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.5

    def items(self):
        p = Plane.objects\
                    .values_list('tailnumber', flat=True)\
                    .order_by()\
                    .distinct()
        
        p = [x.upper() for x in p]
        
        return p
    
    def location(self, item):
        item = item.replace(' ','')
        from django.core.urlresolvers import reverse
        try:
            return reverse("profile-tailnumber", kwargs={"tn": item})
        except:
            return ""
        

class TypeSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.5

    def items(self):
        p = Plane.objects\
                    .values_list('type', flat=True)\
                    .order_by()\
                    .distinct()
        
        p = [x.upper() for x in p]
        
        return p
    
    def location(self, item):
        item = item.replace(' ','')
        from django.core.urlresolvers import reverse
        try:
            return reverse("profile-type", kwargs={"ty": item})
        except:
            return ""
        

class ModelSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.5

    def items(self):
        p = Plane.objects\
                    .values_list('model', flat=True)\
                    .order_by()\
                    .distinct()
        
        return p
    
    def location(self, item):
        item = item.replace(' ','_')
        from django.core.urlresolvers import reverse
        try:
            return reverse("profile-model", kwargs={"model": item})
        except:
            return ""
