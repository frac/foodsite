from tagging.models import Tag
from foodsite.core.models import Post
import datetime
from django.core.cache import cache
import operator

def get_categories(request):
    tags = cache.get('categories')

    if not tags:
        filter = dict(published_at__isnull=False,published_at__lte=datetime.datetime.today())
        tags = Tag.objects.usage_for_model(Post, counts=True, min_count=0, filters=filter)
        tags.sort(key=operator.attrgetter("count"), reverse=True)
        tags = tags[:10]
        cache.set('categories', tags)


    return {
        'categories': tags,
    }


