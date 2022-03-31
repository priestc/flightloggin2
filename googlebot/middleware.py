import os
from django.http import HttpResponse

to_ban =  [
    'googlebot', 'yahoo! slurp', 'bingbot', 'Baiduspider', 'YandexBot',
    'semrushbot', 'dotbot', 'MJ12bot', 'BLEXBot', 'AhrefsBot', 'LieBaoFast',
    'Qwantify', 'CCBot', 'Mb2345Browser', 'MicroMessenger', 'BLEXBot',
    'proximic', 'OPPO A33 Build', 'PetalBot' 
]

class LimitBotsMiddleware(object):
    
    def process_request(self, request):
        """
        Limit googlebot to only see pages between the specefied start and end
        times
        """
        agent = request.META.get('HTTP_USER_AGENT', '').lower()

        is_overloaded = False
        is_bot = False
        for key in to_ban:
            if key.lower() in agent:
                is_bot = True
                is_overloaded = os.getloadavg()[1] > 0.95
                break

        #print agent, str(is_bot), str(is_overloaded)

        if is_bot and is_overloaded:
            return HttpResponse("503 - Spider detected, server overloaded, come back later", status=503)
