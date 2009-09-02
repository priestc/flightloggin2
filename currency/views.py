from annoying.decorators import render_to
from is_shared import is_shared

@render_to('currency.html')
def currency(request, username):
    shared, display_user = is_shared(request, username)
    return locals()
