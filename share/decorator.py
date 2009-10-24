from settings import SECRET_KEY
from django.http import Http404

class no_share(object):
    def __init__(self, view):
        self.view = view
    
    def __call__(self, request, *args, **kwargs):
        """Don't let them in if it's shared"""
        
        if kwargs.get('shared', True):
            from django.http import Http404
            raise Http404('not availiable for sharing')

        return self.view(request, *args, **kwargs)
    
class secret_key(object):
    def __init__(self, view):
        self.view = view
    
    def __call__(self, request, *args, **kwargs):
        """Don't let them in unless they have the secret key"""
        
        secret_key = request.GET.get('sk', '')
      
        if not secret_key:
            raise Http404('Need secret key')
        
        elif not secret_key == SECRET_KEY:
            raise Http404('Secret key incorrect')

        return self.view(request, *args, **kwargs)
    

