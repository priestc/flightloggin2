from models import AwardedBadge

def badge_count(request):
	bc = AwardedBadge.objects.filter(user=request.display_user).count()
	return {'badges_count': bc}