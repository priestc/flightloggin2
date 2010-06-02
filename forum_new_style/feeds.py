from django.contrib.syndication.views import Feed
from django.conf import settings
from models import Forum, Thread, Post

class LatestPostsFeed(Feed):
    title = "%s Forum Posts" % (getattr(settings, "FORUM_NAME") or "", )
    link = "/sitenews/"
    description = "Updates on changes and additions to chicagocrime.org."

    def items(self):
        return Posts.objects.order_by('-posted_time')[:5]

    def item_title(self, item):
        return "%s - %s" % (item.thread.title, item.user or "Anonymous")

    def item_description(self, item):
        return item.body

