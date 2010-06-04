from django.conf.urls.defaults import *
from feeds import *

urlpatterns = patterns('forum_new_style.views',

    url(
        r'^$',
        'index',
        name="index",
    ),
    
    ##########################

    url(
        r'forum/(?P<id>\d+)(?P<slug>[-\w]+)/$',
        'forum_view',
        name='forum',
    ),
    
    url(
        r'forum/(?P<id>\d+)/thread_rss$',
        ForumThreadFeed(),
        name='forum_threads_rss',
    ),
    
    url(
        r'forum/(?P<id>\d+)/post_rss$',
        ForumPostFeed(),
        name='forum_posts_rss',
    ),
    
    ###########################
    
    url(
        r'thread/(?P<id>\d+)(?P<slug>[-\w]+)/$',
        'thread_view',
        name='thread',
    ),
    
    url(
        r'thread/(?P<id>\d+)/post_rss$',
        ThreadPostFeed(),
        name='thread_posts_rss',
    ),
    
    ##########################
    
    url(
        r'delete/(?P<id>\d+)-(?P<timehash>\d+)/$',
        'delete_post',
        name='delete',
    ), 
    
    url(
        r'post_rss$',
        AllPostFeed(),
        name='all_posts_rss',
    ),
    
    url(
        r'thread_rss$',
        AllThreadFeed(),
        name='all_threads_rss',
    ),
)
