import datetime
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
        now = datetime.datetime.now().hour

        in_interval = self.bots_start_hour < now < self.bots_stop_hour
        is_googlebot = 'googlebot' in agent
        is_yahoobot = 'yahoo! slurp' in agent
        if (is_googlebot or is_yahoobot) and not in_interval:
            return HttpResponse("503 - Server Overloaded, come back later", status=503)
