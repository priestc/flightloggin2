from annoying.decorators import render_to
from is_shared import is_shared

@render_to('graphs.html')
def graphs(request, username):
    shared, display_user = is_shared(request, username)
    return locals()
