class no_share(object):
    def __init__(self, view):
        self.view = view
    
    def __call__(self, *args, **kwargs):
        if kwargs.get('shared', False):
            from django.http import Http404
            raise Http404

        return self.view(*args, **kwargs)
