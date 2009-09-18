from settings import SECRET_KEY

class no_share(object):
    def __init__(self, view):
        self.view = view
    
    def __call__(self, *args, **kwargs):
        try:
            secret_key = args[0].GET.get('secret_key')                 #args[0] == request
        except IndexError:
            secret_key = kwargs['request'].GET.get('secret_key')
        except KeyError:
            secret_key = None
        
        if kwargs.get('shared', False) and not secret_key == SECRET_KEY:
                from django.http import Http404
                raise Http404

        return self.view(*args, **kwargs)
