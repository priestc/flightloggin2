import json

from django.http import HttpResponseRedirect, HttpResponse
from django.conf import settings
from django.contrib.auth.decorators import login_required

from share.decorator import secret_key, no_share
from django.views.decorators.cache import cache_page

from states import get_states_data, get_countries_data

@cache_page(60 * 60 * 6)
def states_data(request, type_):
    data = json.dumps(list(get_states_data(request.display_user, type_)))
    return HttpResponse(data, mimetype="application/json")

@cache_page(60 * 60 * 6)
def countries_data(request, type_):
    data = json.dumps(list(get_countries_data(request.display_user, type_)))
    return HttpResponse(data, mimetype="application/json")

@no_share('NEVER')
@login_required
def render_me(request):
    
    render_for_user(request.display_user)

    # return the user to their maps page with spiffy new updated images
    from django.core.urlresolvers import reverse
    url = reverse('maps', args=(request.display_user.username,) )

    return HttpResponseRedirect(url)
