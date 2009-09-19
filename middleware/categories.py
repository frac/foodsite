from tagging.models import Tag
from foodsite.core.models import Post
import datetime

def get_categories(request):
    filter = dict(published_at__isnull=False,published_at__lte=datetime.datetime.today())

    tags = Tag.objects.usage_for_model(Post, counts=True, min_count=1, filters=filter)


    return {
        'categories': tags,
    }


