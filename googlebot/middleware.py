import os
from django.http import HttpResponse

class LimitBotsMiddleware(object):
    
    def process_request(self, request):
        """
        Limit googlebot to only see pages between the specefied start and end
        times
        """
        agent = request.META.get('HTTP_USER_AGENT', '').lower()

        is_overloaded = False
        is_bot = False
        for key in ['googlebot', 'yahoo! slurp', 'bingbot', 'Baiduspider', 'YandexBot']:
            if key in agent:
                is_bot = True
                is_overloaded = os.getloadavg()[1] > 3
                break

        if is_bot and is_overloaded:
            return HttpResponse("503 - Spider detected, server overloaded, come back later", status=503)
