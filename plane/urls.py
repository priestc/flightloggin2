from django.conf.urls.defaults import *
from models import Plane

from django.conf import settings
username_regex = settings.REGEX_USERNAME

urlpatterns = patterns('plane.views',
    url(r'^tailnumber/(?P<tn>%s+)$' % Plane.plane_regex, "tailnumber_profile", name="profile-tailnumber"),
    url(r'^type/(?P<ty>%s+)$' % Plane.plane_regex, "type_profile", name="profile-type"),
    url(r'^model/(?P<model>.+)$', "model_profile", name="profile-model"),
    url(r'^mass/(?P<username>%s)$' % username_regex, "mass_planes", name="mass-planes"),
    url(r'(?P<username>%s)\.json' % username_regex, 'user_planes'),
    url(r'(?P<username>%s)$' % username_regex, "planes", name="planes"),
    url(r'^search/tailnumbers$', 'search_tailnumbers'),
)