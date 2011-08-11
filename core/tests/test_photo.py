from django.test import TestCase

from django.core.files import File

from foodsite.core.models import Photo
from foodsite.settings import SITE_URL, MEDIA_URL

import os.path

class TestPhoto(TestCase):
    def setUp(self):
        self.p = Photo()
    def tearDown(self):
        """
        if the picture exists I should delete to avoid leftover files
        """
        if self.p.id:
            self.p.delete()
        
    """
    Tests the picture part of the blog. 
    """
    def test_image_creation_and_deletion(self):
        """
        """

        f = File(open("core/tests/test_images/test.jpg", "r"))
        p = self.p
        p.title = "test"
        p.image.save("testfile.jpg", f)
        p.save()
        
        #I save the images path
        full_pic = p.image.path
        small_pic = p.get_path(thumb=False)
        thumb_pic = p.get_path(thumb=True)

        #they should exist
        self.assertTrue(os.path.isfile(full_pic))
        self.assertTrue(os.path.isfile(small_pic))
        self.assertTrue(os.path.isfile(thumb_pic))

        p.delete()

        # and they should not exist anymore
        self.assertFalse(os.path.isfile(full_pic))
        self.assertFalse(os.path.isfile(small_pic))
        self.assertFalse(os.path.isfile(thumb_pic))


    def test_image_properties(self):
        """
        See if associated props are there.
        Those are important for the admin and templates
        """

        f = File(open("core/tests/test_images/test.jpg", "r"))
        p = self.p
        p.title = "test"
        p.image.save("NEW_testfile.jpg", f)
        p.save()

        self.assertTrue("NEW_testfile_t.jpg" in p.thumb)
        self.assertTrue("NEW_testfile_s.jpg" in p.small)
        self.assertTrue("NEW_testfile_s.jpg" in p.full_url)
        self.assertTrue(MEDIA_URL in p.full_url)
        self.assertTrue(SITE_URL in p.wave)
        self.assertTrue("photowave" in p.wave)
        self.assertTrue(str(p.id) in p.wave)


