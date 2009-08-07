from annoying.decorators import render_to
from annoying.functions import get_object_or_None
from forms import ProfileForm, ColumnsForm

@render_to("preferences.html")
def profile(request):
    title="Preferences"
    profile_form = ProfileForm()
    column = ColumnsForm()

    return locals()
