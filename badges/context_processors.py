from models import AwardedBadge
from django.db.models import Sum

def badge_count(request):
	u = getattr(request, 'display_user', None)
	bc = AwardedBadge.objects.filter(user=u).aggregate(s=Sum('level'))['s']
	return {'badges_count': bc}