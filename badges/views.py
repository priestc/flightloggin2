from models import AwardedBadge
from annoying.decorators import render_to

@render_to('badges.html')
def badges(request):
    badges = AwardedBadge.objects.filter(user=request.display_user).order_by('-awarded_date')
    return locals()