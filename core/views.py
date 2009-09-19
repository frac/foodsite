# Create your views here.
from django.contrib.syndication.feeds import Feed
from django.utils.feedgenerator import Atom1Feed

from django.views.generic.list_detail import object_list

import datetime
from core.models import Post



def list(request):
    posts =  Post.get_open()
    page = request.GET.get("page",1) #pagination is 1 based
    return object_list(request, queryset=posts, page=page, paginate_by=10)


class BlogFeed(Feed):
    title = "Secret Food Project"
    link = "/"
    description = "Food obsession is an art"

    def item_link(self, item):
        """
        Takes an item, as returned by items(), and returns the item's URL.
        """
        return "/post/%s"% item.slug

    def items(self):
        return Post.objects.filter(published_at__isnull=False,published_at__lte=datetime.datetime.today()).order_by('-published_at')[:10]

class AtomBlogFeed(BlogFeed):
    feed_type = Atom1Feed
    subtitle = BlogFeed.description
