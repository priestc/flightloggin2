def hash_ten(value, length=10):
    import hashlib;
    m = hashlib.sha256()
    m.update(str(value))
    return m.hexdigest()[:length]


from django.http import HttpResponse
from django.utils import simplejson
from django.core.mail import mail_admins
from django.utils.translation import ugettext as _
import sys


def json_view(func):
    """
    http://www.djangosnippets.org/snippets/622/
    """
    
    def wrap(request, *a, **kw):
        response = None
        try:
            func_val = func(request, *a, **kw)
            assert isinstance(func_val, dict)
            response = dict(func_val)
            if 'result' not in response:
                response['result'] = 'ok'
        except KeyboardInterrupt:
            # Allow keyboard interrupts through for debugging.
            raise
#        except Exception, e:
#            # Mail the admins with the error
#            exc_info = sys.exc_info()
#            subject = 'JSON view error: %s' % request.path
#            try:
#                request_repr = repr(request)
#            except:
#                request_repr = 'Request repr() unavailable'
#            import traceback
#            message = 'Traceback:\n%s\n\nRequest:\n%s' % (
#                '\n'.join(traceback.format_exception(*exc_info)),
#                request_repr,
#                )
#            mail_admins(subject, message, fail_silently=True)

#            # Come what may, we're returning JSON.
#            if hasattr(e, 'message'):
#                msg = e.message
#            else:
#                msg = _('Internal error')+': '+str(e)
#            response = {'result': 'error',
#                        'text': msg}

        json = simplejson.dumps(response)
        return HttpResponse(json, mimetype='application/json')
    return wrap

def ajax_timestamp_to_datetime(s):
    """
    2010-02-03--20.23.13 to a datetime object
    """
    import datetime
    return datetime.datetime.strptime(s, '%Y-%m-%d--%H.%M.%S')










