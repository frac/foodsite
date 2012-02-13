from django.test import TestCase

from foodsite.middleware.categories import get_categories
from foodsite.core.models import Post
from tagging.models import Tag

from django.core.cache import cache


class TestMiddleware(TestCase):
    """
    Check to see if the middleware works
    """

    def test_return(self):
        self.assertEqual(get_categories({}),{"categories":[]})
        p1 = Post.objects.create(title="foo",slug="foo",text="foo")
        Tag.objects.update_tags(p1, "cheese,grilled")
        #Not published and cached
        self.assertEqual(get_categories({}),{"categories":[]})
        cache.set('categories', None)
        #not published so still not appearing
        self.assertEqual(get_categories({}),{"categories":[]})

        p1.published_at = "2000-01-01 10:10"
        p1.save()
        Tag.objects.update_tags(p1, "cheese,grilled")

        cache.set('categories', None)
        self.assertEqual(len(get_categories({})["categories"]),2)

        Tag.objects.update_tags(p1, "a,b,c,d,e,f,g,k,l,m,n,o,p")

        cache.set('categories', None)
        self.assertEqual(len(get_categories({})["categories"]),10)



