from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect

from annoying.decorators import render_to
from annoying.functions import get_object_or_None

#from forms import *

@render_to('import.html')
def import_s(request):
    title = "Import/Export"
    return locals()
