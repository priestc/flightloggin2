from django.conf.urls.defaults import *

urlpatterns = patterns('forum_new_style.views',

    url(
        r'^$',
        'index',
        name="index",
    ),

    url(
        r'forum-(?P<id>\d+)(?P<slug>[-\w]+)/',
        'forum_view',
        name='forum',
    ),
    
    url(
        r'thread-(?P<id>\d+)(?P<slug>[-\w]+)/',
        'thread_view',
        name='thread',
    ),
    
    url(
        r'delete-(?P<id>\d+)-(?P<timehash>\d+)/',
        'delete_post',
        name='delete',
    ),
)
