from models import AwardedBadge
from django.db.models import Sum

def badge_count(request):
	return {}	
	# displaying the total for the user that own the page
	u = getattr(request, 'display_user', None)

	logged_in = request.user.is_authenticated()
	if not u and logged_in:
		u = request.user
	if not u and not logged_in:
		u = None
	
	bc = AwardedBadge.objects.filter(user=u).aggregate(s=Sum('level'))['s']
	
	return {'badges_count': bc or 0}
