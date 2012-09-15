import requests

from annoying.decorators import render_to
from django.http import HttpResponse, Http404
from django.views.decorators.cache import cache_page

@render_to('products.html')
def twice_scroll(request, category):
	categories = ("dresses", "pants", "all", "tops", "jeans", "skirts")
	if category not in categories:
		raise Http404('category not found')
	return {'category': category, "categories": categories}

@cache_page(30 * 60)
def products_proxy(request, page, category):
	"""
	Since the front end can't access liketwice directly due to cross domain
	retrictions, this view acts as a proxy (and a cache).
	"""
	url = "https://www.liketwice.com/ajax/shop/items?category=%s&page=%s" % (category, page)
	data = requests.get(url).content
	return HttpResponse(data, mimetype="application/json")