from django.db import models
from django.db.models.signals import post_save, pre_delete
from tagging.fields import TagField
from tagging.models import Tag

import Image, os, ImageOps
MAX_SIZE = 970
SMALL_SIZE = 450
THUMB_SIZE = 210

# Create your models here.
class Photo(models.Model):
    title = models.CharField(max_length=255)
    image = models.ImageField(upload_to='photos/%Y/%m/%d')

    def __unicode__(self):
        return u"%s"% (self.title)

    @property
    def thumb(self):
        path = str(self.image)
        return "%s_t%s"% (path[:-4],path[-4:])

    @property
    def small(self):
        path = str(self.image)
        return "%s_s%s"% (path[:-4],path[-4:])

    def get_path(self, thumb=True):
        if thumb:
            return "%s_t%s"% (self.image.path[:-4],self.image.path[-4:])
        else:
            return "%s_s%s"% (self.image.path[:-4],self.image.path[-4:])

    def create_thumb(self):
        im = Image.open(self.image )
        format = im.format
        min_dim = min(im.size)
#        im = im.crop((0,0,min_dim,min_dim))

        #make large
        im.thumbnail((MAX_SIZE,MAX_SIZE), Image.ANTIALIAS)
        im.save(self.image.path, format)

        #make it square
        im = ImageOps.fit(im, (min_dim,min_dim), centering=(0.5, 0.5))

        #make small 
        im.thumbnail((SMALL_SIZE,SMALL_SIZE), Image.ANTIALIAS)
        im.save(self.get_path(thumb=False), format)

        # create the path for the thumbnail image
        #thumb_path = self.thumb_path()
        #thumb_dir = os.path.dirname(thumb_path)
        #if not os.path.exists(thumb_dir):
        #    os.makedirs(thumb_dir, 0775)

        # Make Thumb
        im.thumbnail((THUMB_SIZE,THUMB_SIZE), Image.ANTIALIAS)
        im.save(self.get_path(), format)

    def destroy_thumb(self):
        try:
            os.unlink(self.thumb)
        except:
            pass

    
def cria_visualizacao(sender, **kwargs):
    instance = kwargs["instance"]
    if instance.image:
        #if not sender.thumb_exists():
        instance.create_thumb()
    
def destroy_visualizacao(sender, **kwargs):
    instance = kwargs["instance"]
    instance.destroy_thumb()


post_save.connect(cria_visualizacao, sender=Photo)
pre_delete.connect(destroy_visualizacao, sender=Photo)

class Post(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField()
    text = models.TextField()
    pic = models.ForeignKey(Photo, null=True, blank=True)
    published_at = models.DateTimeField(null=True, blank=True)
    tags = TagField()

    def set_tags(self, tags):
        Tag.objects.update_tags(self, tags)

    def get_tags(self, tags):
        return Tag.objects.get_for_object(self)    

    def __unicode__(self):
        return u"%s"% self.title

class Recipe(Post):
    pass

class Ingredient(Post):
    def __unicode__(self):
        return u"%s"% (self.title)

CONVERSIONS= ((0,"gramas"),
              (1,"kilos"),
              (3,"celcius")  
            )

class Unit(models.Model):
    metric = models.CharField(max_length=255)
    imperial = models.CharField(max_length=255)
    conversion = models.IntegerField(choices=CONVERSIONS)

    def get_metric(self):
        pass
    
    def get_imperial(self):
        pass

    def __unicode__(self):
        return u"%s,%s"% (self.metric, self.imperial)

class Measurement(models.Model):
    recipe = models.ForeignKey(Recipe)
    ingredient = models.ForeignKey(Ingredient)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    unit = models.ForeignKey(Unit)
    order = models.IntegerField()

    

    
