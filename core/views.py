# Create your views here.
from django.contrib.syndication.feeds import Feed
from django.utils.feedgenerator import Atom1Feed

from django.views.generic.list_detail import object_list

import datetime
from foodsite.core.models import Post



def list(request):
    posts =  Post.get_open()
    page = request.GET.get("page",1) #pagination is 1 based
    return object_list(request, queryset=posts, page=page, paginate_by=5)


class BlogFeed(Feed):
    title = "Secret Food Project"
    link = "/"
    description = "So secret that we don't even have a subtitle"

    def item_link(self, item):
        """
        Takes an item, as returned by items(), and returns the item's URL.
        """
        return "/post/%s"% item.slug

    def item_pubdate(self, item):
        """
        Takes an item, as returned by items(), and returns the item's
        pubdate.
        """        
        return item.published_at

    def item_author_name(self, item):
        """
        Returns the author name for every item in the feed.
        """
        return item.author

    def items(self):
        return Post.get_open()[:10]

class AtomBlogFeed(BlogFeed):
    feed_type = Atom1Feed
    subtitle = BlogFeed.description
    author_name="Adriano Petrich"


