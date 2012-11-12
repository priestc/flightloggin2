from django.conf.urls.defaults import *
from models import Plane

urlpatterns = patterns('plane.views',
    url(r'^tailnumber/(?P<tn>%s+)$' % Plane.plane_regex, "tailnumber_profile", name="profile-tailnumber"),
    url(r'^type/(?P<ty>%s+)$' % Plane.plane_regex, "type_profile", name="profile-type"),
    url(r'^model/(?P<model>.+)$', "model_profile", name="profile-model"),
    url(r'^mass/(?P<username>\w+)$', "mass_planes", name="mass-planes"),
    url(r'(?P<username>\w+)$', "planes", name="planes"),
    url(r'^search/tailnumbers$', 'search_tailnumbers'),
)