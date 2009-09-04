from annoying.decorators import render_to
from is_shared import is_shared

@render_to('currency.html')
def currency(request, username):
    shared, display_user = is_shared(request, username)
    
    from FAA import FAA_Currency
    
    faa = FAA_Currency(display_user)
    
    
    
    
    return locals()
