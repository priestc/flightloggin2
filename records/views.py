from annoying.decorators import render_to
from annoying.functions import get_object_or_None

@render_to("records.html")
def records(request):
    title="records"
    return locals()
