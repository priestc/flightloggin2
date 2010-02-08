from django.views.decorators.cache import cache_page
from histogram import *

@cache_page(60 * 60 * 3)
def model(request, model=None):
    b = ModelSpeedHistogram(model=model)
    return b.as_png()

@cache_page(60 * 60 * 3)
def user_totals(request, model=None):
    b = UserTotalsHistogram()
    return b.as_png()

@cache_page(60 * 60 * 3)
def type_(request, type_=None):
    b = TypeSpeedHistogram(type_=type_)
    return b.as_png()
