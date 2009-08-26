from annoying.decorators import render_to
from is_shared import is_shared

@render_to('stats.html')
def stats(request, username):
    shared, display_user = is_shared(request, username)
    return locals()
