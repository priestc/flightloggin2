from annoying.decorators import render_to
from share.decorator import no_share

@no_share('other')
@render_to('maps.html')
def maps(request):
    return {"map_height": 'tall'}
