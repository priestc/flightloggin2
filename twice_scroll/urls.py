from django.conf.urls.defaults import *

urlpatterns = patterns('twice_scroll',
    url(r'scroll-(?P<category>\w+)', 'views.twice_scroll', name="twice_scroll"),
    (r'products-(?P<category>\w+)-(?P<page>\d{1,5})', 'views.products_proxy'),
)