from models import Badge
from annoying.decorators import render_to

@render_to('badges.html')
def badges_view(request):
    badges = Badge.objects.filter(user=request.display_user)
    return locals()