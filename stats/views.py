from annoying.decorators import render_to

@render_to('stats.html')
def stats(request):
    return locals()
