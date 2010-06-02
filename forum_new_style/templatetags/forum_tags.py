from django import template

register = template.Library()

def post_render(post, viewing_user, viewing_ip):

    admin_rights = False
    if viewing_ip == post.ip or viewing_user == post.user or viewing_user.is_staff:
        admin_rights = True
    
    c = {'post': post, 'viewing_user': viewing_user, 'admin_rights': admin_rights}
    return template.loader.render_to_string('post.html', c)

register.simple_tag(post_render)
