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
        Return all threads ordered by last bumped datetimeas a queryset
        annotated with 'bumped'
        (vbulletin style)
        """
        
        return self.thread_set\
                   .annotate(bumped=models.Max('post__posted_time'))\
                   .order_by('-bumped').select_related()
                   
    def threads_by_op(self):
        """
        Return all threads ordered by date of the first post as a queryset
        annotated with 'bumped'
        (google groups style)
        """
        
        return self.thread_set\
                   .annotate(bumped=models.Min('post__posted_time'))\
                   .order_by('-bumped').select_related()
    
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
        Return the first post in this thread
        """
        
        op = self.post_set.order_by('posted_time').select_related()
        
        if not op:
            return Post()
               
        return op[0]
    op = property(op)
    
    def last_bumped(self):
        """
        Returs a datetime object of when the last post was made in this thread
        """

        try:
            return self.post_set\
                       .values_list('posted_time', flat=True)\
                       .order_by('-posted_time')[0]
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
    
    class Meta:
        ordering = ['-posted_time', ]
    
    def get_absolute_url(self):
        return self.thread.get_absolute_url() + "#%s" % self.pk
    
    def __unicode__(self):
        return "%s - %s" % (self.posted_time,
                            getattr(self.user, "username", "Anon"))
    
    def timehash(self):
        """
        Return a hash derived from the time the post was made.
        Used to authenticate the post before it gets deleted
        """
        
        return self.posted_time.microsecond
    
    def poster(self):
        """
        Print out the name of the user who has made this post with respect
        to the anonymity the user has chosen.
        """
        
        if self.as_anon and not self.as_admin:
            return "Anonymous"
        elif self.as_anon and self.as_admin:
            return "Admin"
        else:
            return self.user.username
