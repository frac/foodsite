from django.test import TestCase

from foodsite.core.templatetags import foodtags as ft
from foodsite.core.models import Post, Recipe

class TestTemplateTaga(TestCase):
    """
    Useful template tags
    """

    def test_ingredients(self):
        """
        show ingredient list for recipes, not for posts
        """
        p = Post.objects.create(title="foo", slug="foo", text="foo")
        self.assertEqual(ft.ingredients(p), "")

        r = Recipe.objects.create(title="foo", slug="foo", text="foo")
        self.assertNotEqual(ft.ingredients(r), "")


    def test_no_img(self):
        """
        strips textile imgs from text
        """
        self.assertEqual(ft.no_img("!abc!dfg"),"dfg")
        self.assertEqual(ft.no_img("abc!dfg"),"abc!dfg")
        

