import os
from django.http import HttpResponse

class LimitBotsMiddleware(object):
    bots_start_hour = 2
    bots_stop_hour =  10
    
    def process_request(self, request):
        """
        Limit googlebot to only see pages between the specefied start and end
        times
        """
        agent = request.META.get('HTTP_USER_AGENT', 'what').lower()

        overloaded = os.getloadavg()[2] > 3

        is_googlebot = 'googlebot' in agent
        is_yahoobot = 'yahoo! slurp' in agent
        is_bingbot = 'bingbot' in agent
        if (is_googlebot or is_yahoobot or is_bingbot) and overloaded:
            return HttpResponse("503 - Server Overloaded, come back later", status=503)
