from django import template
from django.core.urlresolvers import reverse

from forum_new_style.models import *

def post_render(post, viewing_user, viewing_ip):

    admin_rights = False
    if viewing_ip == post.ip or viewing_user == post.user or viewing_user.is_staff:
        admin_rights = True
    
    c = {'post': post, 'viewing_user': viewing_user, 'admin_rights': admin_rights}
    return template.loader.render_to_string('post.html', c)

def rss_markup(obj, items=None):
    """
    Return the rendered RSS tag for insertion into a template
    """
    
    rss = '<link rel="alternate" title="%s" href="%s" type="application/rss+xml">'
    context = {}
    kwargs = {}
    
    #############
    
    if obj == 'all':
        context.update({'type': 'all', 'name': 'All'})
        
    elif isinstance(obj, Thread):
        context.update({'name': obj.title, 'type': 'thread', 'id': obj.pk})
        kwargs={'id': obj.pk}
        
    elif isinstance(obj, Forum):
        context.update({'name': obj.name, 'type': 'forum', 'id': obj.pk})
        kwargs={'id': obj.pk}
        
    #############
    print items
    if items == 'threads':
        context.update({'items': 'threads'})
    
    elif items == 'posts':
        context.update({'items': 'posts'})
        
    #############
    
    named_url = 'forum:%(type)s_%(items)s_rss' % context
    url = reverse(named_url, kwargs=kwargs)
    title = "%(name)s %(items)s feed" % context
    return rss % (title, url)
    
register = template.Library()
register.simple_tag(rss_markup)
register.simple_tag(post_render)
