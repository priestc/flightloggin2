from django.contrib.syndication.views import Feed
from django.conf import settings
from django.db.models import Min
from django.shortcuts import get_object_or_404
from django.utils.dateformat import format

from models import Forum, Thread, Post

overall_name = getattr(settings, "FORUM_OVERALL_NAME", '')

class GenericThreadFeed(Feed):

    def item_title(self, thread):
        date = format(thread.op.posted_time, 'Y M d, G:i T')
        return "%s -- %s (%s)" % (thread.title, thread.op.poster(), date)

    def item_description(self, thread):
        return thread.op.body + "\n\n---\nPlus %s replies" % thread.post_count()

    def link(self):
        return 'ff'

class ForumThreadFeed(GenericThreadFeed):
    """
    Feed of all threads in one forum
    """
    
    def get_object(self, request, id):
        """
        Get and return the forum object that was passed in
        """
        return get_object_or_404(Forum, pk=id)
    
    def items(self, forum):
        """
        Return the last 20 threads made in this forum,
        sorted by op creation date
        """
        return forum.threads_by_op()[:20]
    
    def title(self, obj):
        if overall_name:
            disp = " (%s)" % overall_name
        else:
            disp = ""
        return "%s Threads %s" % (obj.name, disp)
        
    def link(self, forum):
        return forum.get_absolute_url()
    
class AllThreadFeed(GenericThreadFeed):
    """
    Feed of all threads across all forums
    """

    def items(self):
        """
        Return the last 20 threads made in any forum,
        sorted by op creation date
        """
        return Thread.objects\
                      .annotate(bumped=Min('post__posted_time'))\
                      .order_by('-bumped')\
                      .select_related()[:20]
        
    def title(self, obj):
        if overall_name:
            disp = " (%s)" % overall_name
        else:
            disp = ""
        return "All Threads %s" % disp
    
######################

class GenericPostFeed(Feed):   
    
    def item_title(self, post):
        date = format(post.posted_time, 'Y M d, G:i T')
        return "%s -- %s (%s)" % (post.thread.title, post.poster(), date)

    def item_description(self, post):
        return post.body

    def link(self, post):
        return "ff"


class ForumPostFeed(GenericPostFeed):
    """
    Feed of all posts from a forum
    """
        
    def get_object(self, request, id):
        return get_object_or_404(Forum, pk=id)

    def items(self, forum):
        """
        Return the last 20 post made in this forum,
        sorted by creation date
        """
        return Post.objects\
                   .filter(thread__forum=forum)\
                   .order_by('-posted_time')[:20]
    
    def title(self, forum):
        if overall_name:
            disp = " (%s)" % overall_name
        else:
            disp = ""
        return "%s Posts %s" % (forum.name, disp)


class ThreadPostFeed(GenericPostFeed):
    """
    Feed of all posts from a thread
    """
    
    def get_object(self, request, id):
        return get_object_or_404(Thread, pk=id)

    def items(self, thread):
        """
        Return the last 20 post made in this thread,
        sorted by creation date
        """
        return Post.objects\
                   .filter(thread=thread)\
                   .order_by('-posted_time')[:20]
    
    def title(self, thread):
        if overall_name:
            disp = " (%s)" % overall_name
        else:
            disp = ""
        return "Posts in thread '%s' %s" % (thread.title, disp)


class AllPostFeed(GenericPostFeed):
    """
    Feed of all posts across all forums
    """

    def items(self):
        """
        Return the last 20 threads made in any forum,
        sorted by op creation date
        """
        return Post.objects.select_related()[:20]
                      
        
    def title(self, obj):
        if overall_name:
            disp = " (%s)" % overall_name
        else:
            disp = ""
        return "All Posts %s" % disp






