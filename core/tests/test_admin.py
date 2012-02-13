from django.test import TestCase

from django.test.client import Client 
from django.contrib.auth.models import User
from django.core.files import File

from foodsite.core.models import Recipe, Photo, Post
from foodsite.core import admin


class TestAdmin(TestCase):
    """
    test if we have admin installed and the correct models there
    """
    def setUp(self):
        self.client = Client()
        u = User.objects.create(username="admin",is_superuser=True)
        u.set_password("admin")
        u.save()
        resp = self.client.login(username='admin', password='admin')
        self.assertTrue(resp)
         
    def test_basic_admin(self):
        """
        is admin there
        """
        resp = self.client.get("/admin/")
        self.assertEquals(resp.status_code, 200)

    def test_core_models_admin(self):
        """
        are the core models registered
        """
        resp = self.client.get("/admin/core/post/add/")
        self.assertEquals(resp.status_code, 200, "post not found")
        resp = self.client.get("/admin/core/recipe/add/")
        self.assertEquals(resp.status_code, 200, "recipe not found")
        resp = self.client.get("/admin/core/photo/add/")
        self.assertEquals(resp.status_code, 200, "photo not found")
        resp = self.client.get("/admin/core/unit/add/")
        self.assertEquals(resp.status_code, 200, "unit not found")
        resp = self.client.get("/admin/core/ingredient/add/")
        self.assertEquals(resp.status_code, 200, "ingredient not found")

    def test_inlines_and_other_mythical_monsters_for_recipes(self):
        """
        Not a functional test.
        Just look at the admin.py file
        """
        
        self.assertEquals(admin.RecipeAdmin.inlines, [admin.MeasurementInline])
        self.assertEquals(admin.RecipeAdmin.list_display, ('title', 'wave', 'pic', 'slug', 'tags', 'published_at'))
        self.assertEquals(admin.RecipeAdmin.actions, [admin.publish])
        self.assertEquals(admin.RecipeAdmin.ordering, ('-published_at',))
        self.assertEquals(admin.RecipeAdmin.prepopulated_fields, {"slug": ("title",)})

    def test_inlines_and_other_mythical_monsters_for_posts(self):
        """
        same for posts
        """
        
        self.assertEquals(admin.PostAdmin.list_display, ('title','pic','slug','published_at'))
        self.assertEquals(admin.PostAdmin.actions, [admin.publish])
        self.assertEquals(admin.PostAdmin.ordering, ('-published_at',))
        self.assertEquals(admin.PostAdmin.prepopulated_fields, {"slug": ("title",)})
        
    def test_inlines_and_other_mythical_monsters_for_ingredients(self):
        """
        same for IngredientAdmin
        """
        self.assertEquals(admin.IngredientAdmin.prepopulated_fields, {"slug": ("title",)})
        self.assertEquals(admin.IngredientAdmin.list_display, ('title','pic'))
        self.assertEquals(admin.IngredientAdmin.ordering, ('pic',))

    def test_inlines_and_other_mythical_monsters_for_photos(self):
        """
        same for PhotoAdmin
        """
        self.assertEquals(admin.PhotoAdmin.actions, [admin.use_photo])
        self.assertEquals(admin.PhotoAdmin.list_display, ('title','used','full_url', 'wave'))
        self.assertEquals(admin.PhotoAdmin.list_filter, ('used',))
    
    def test_inlines_and_other_mythical_monsters_for_units(self):
        """
        same for UnitAdmin
        """
        self.assertEquals(admin.UnitAdmin.list_display, ('metric','imperial','conversion'))


    def test_custom_image_filter_for_recipes(self):
        """
        this is tricky I want to list only the unused pictures in the combo for the recipe.pic

        """
        from foodsite.core import admin
        
        self.check_custom_image_filter_for_modelAdmin(admin.RecipeAdmin(Recipe,{}))

    def test_custom_image_filter_for_posts(self):
        """
        the same for posts
        Show only the pictures that are either not used, or belongs to a post
        """
        
        self.check_custom_image_filter_for_modelAdmin(admin.PostAdmin(Post,{}))

    def check_custom_image_filter_for_modelAdmin(self, modelAdmin):
        """
        The conditions for the image to be on the query are pics with the is_used=False(default)

        I am stubbing the resquest and the db_field
        """
        request = {}
        class foo(object):
            name = "pic"
            def formfield(self, **kwargs):
                self.args = kwargs
        db_field = foo()
        modelAdmin.formfield_for_foreignkey(db_field, request)
        # So far so good
        queryset = db_field.args["queryset"]
        
        #no images found
        self.assertEqual(queryset.count(),0)
        
        # Now I create 3 files to the 3 conditions to see if the query finds only two
        f = File(open("core/tests/test_images/test.jpg", "r"))
        p1 = Photo()
        p1.title = "test1"
        p1.image.save("testfile1.jpg", f)
        p1.save()


        f = File(open("core/tests/test_images/test.jpg", "r"))
        p2 = Photo()
        p2.title = "test2"
        p2.image.save("testfile2.jpg", f)
        # this should not apear
        p2.used = True
        p2.save()

        f = File(open("core/tests/test_images/test.jpg", "r"))
        p3 = Photo()
        p3.title = "test3"
        p3.image.save("testfile3.jpg", f)
        p3.used = True
        p3.save()
        Post.objects.create(title="foo",slug="foo",text="foo",pic=p3)
        
        #Finding only p1 and p3
        self.assertEqual(queryset.count(),2)
    
        p1.delete()            
        p2.delete()            
        p3.delete()            














