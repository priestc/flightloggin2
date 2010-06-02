from django.db import models
from django.conf import settings
from django.template.defaultfilters import slugify
from django.core.urlresolvers import reverse

class Forum(models.Model):
    name = models.TextField("The name of the forum (or divider)", blank=False)
    description = models.TextField("Description of the forum", blank=True)
    order = models.IntegerField(default=0)
    force_anon = models.BooleanField(default=False)
    divider = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['order',]
    
    def get_absolute_url(self):
        slug = '-' + slugify(self.name)
        return reverse('forum:forum', kwargs={'id': self.pk, 'slug': slug})
    
    def __unicode__(self):
        return self.name
    
    def post_count(self):
        return Post.objects.filter(thread__forum=self).count()
    
    def thread_count(self):
        return self.thread_set.count()
    
    def last_post(self):
        """
        The date of the last post in this forum
        """
        
        try:
            return self.threads_by_bumped()[0].bumped
        except IndexError:
            return "Never"
    
    def threads_by_bumped(self):
        """
        Return all threads ordered by last bumped datetime
        """
        
        return self.thread_set\
                   .annotate(bumped=models.Max('post__posted_time'))\
                   .order_by('-bumped')
                   
    def threads_by_op(self):
        """
        Return all threads ordered by date of the first post
        """
        
        return self.thread_set\
                   .annotate(bumped=models.Min('post__posted_time'))\
                   .order_by('-bumped')
    
class Thread(models.Model):
    forum = models.ForeignKey(Forum)
    title = models.CharField(max_length=64)
    
    def get_absolute_url(self):
        slug = '-' + slugify(self.title)
        return reverse('forum:thread', kwargs={'id': self.pk, 'slug': slug})
    
    def __unicode__(self):
        return self.title
    
    def post_count(self):
        return self.post_set.count()
    
    def op(self):
        """
        Return the name of the user who made the first post in this thread
        """
        
        op = self.post_set\
                 .values_list('user__username', flat=True)\
                 .order_by('posted_time')
        
        if not op:
            return "Nobody"
               
        return op[0] or "Anonymous"

    
    def last_bumped(self):
        lb = self.post_set\
                 .values_list('posted_time', flat=True)\
                 .order_by('-posted_time')
        
        try:
            return lb[0]
        except IndexError:
            # thread has no posts for whatever reason
            return "Never"
    
class Post(models.Model):
    thread = models.ForeignKey(Thread)
    parent = models.ForeignKey('self', null=True, blank=True)
    body = models.TextField(blank=False)
    user = models.ForeignKey('auth.user', blank=True, null=True)
    posted_time = models.DateTimeField(auto_now=True)
    as_anon = models.BooleanField("Post Anonymously?", default=False)
    as_admin = models.BooleanField("Post as Admin?", default=False)
    flagged = models.BooleanField('Flag this post as spam', default=False)
    ip = models.IPAddressField(default="0.0.0.0") 
    
    def __unicode__(self):
        return "%s - %s" % (self.posted_time, getattr(self.user, "username", "Anon"))
    
    def timehash(self):
        """
        Return a hash derived from the time the post was made.
        Used to authenticate the post before it gets deleted
        """
        
        return self.posted_time.microsecond
