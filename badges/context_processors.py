from models import AwardedBadge
from django.db.models import Sum

def badge_count(request):
	u = getattr(request, 'display_user', None)
	bc = 0
	if not u and request.user.is_authenticated():
		u = request.user
		bc = AwardedBadge.objects.filter(user=u).aggregate(s=Sum('level'))['s']
	
	return {'badges_count': bc or 0}