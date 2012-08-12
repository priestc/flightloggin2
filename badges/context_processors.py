from models import AwardedBadge

def badge_count(request):
	u = getattr(request, 'display_user', None)
	bc = AwardedBadge.objects.filter(user=u).count()
	return {'badges_count': bc}