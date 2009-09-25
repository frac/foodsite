from django.db import models
from django.db.models.signals import post_save, pre_delete
from django.core.cache import cache
from tagging.fields import TagField
from tagging.models import Tag
import datetime
import Image, os, ImageOps
MAX_SIZE = 970
SMALL_SIZE = 450
THUMB_SIZE = 210

# Create your models here.
class Photo(models.Model):
    title = models.CharField(max_length=255)
    image = models.ImageField(upload_to='photos/%Y/%m/%d')
    author = models.CharField(max_length=255, default="Adriano")

    class Meta:
        ordering = ["-image"]

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

    @property
    def full_url(self):
        path = str(self.image)
        return "http://sfp.adrianopetrich.com/static/%s_s%s"% (path[:-4],path[-4:])

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
            os.unlink(self.get_path(True))
            os.unlink(self.get_path(False))
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
    slug = models.SlugField(unique=True)
    text = models.TextField()
    pic = models.ForeignKey(Photo, null=True, blank=True)
    published_at = models.DateTimeField(null=True, blank=True)
    tags = TagField()
    author = models.CharField(max_length=255, default="Adriano")
    
    @property
    def enable_comments(self):
        return True

    @property
    def full_url(self):
        return "http://sfp.adrianopetrich.com/post/%s"% self.slug

    class Meta:
        ordering = ["-published_at"]

    def set_tags(self, tags):
        Tag.objects.update_tags(self, tags)

    def get_tags(self):
        return Tag.objects.get_for_object(self)    

    def __unicode__(self):
        return u"%s"% self.title

    def get_next(self):
        try:
            self._next
        except AttributeError:
            self._next = None
        try:
            if self._next == None:
                self._next = Post.get_open().filter(published_at__gt=self.published_at).order_by("published_at")[0]
            return self._next
        except:
            return None

    def get_previous(self):
        try:
            self._previous
        except AttributeError:
            self._previous = None
        try:

            if self._previous == None:
                self._previous = Post.get_open().filter(published_at__lt=self.published_at).order_by("-published_at")[0]
            return self._previous
        except:
            return None
    
    
    @staticmethod
    def get_open():
        return Post.objects.filter(published_at__isnull=False,published_at__lte=datetime.datetime.today()).order_by('-published_at')

class Recipe(Post):
    pass

class Ingredient(Post):
    @property
    def name(self):
        return self.title

CONVERSIONS= (
              (0,"No conversion"),
              (1,"g/oz"),
              (2,"k/Lb"),
              (3,"ml/foz"),
              (8,"ml/cup"),
              (4,"l/foz"),
              (9,"l/quart"),
              (5,"cm/inch"),
              (6,"m/inch"),
              (10,"m/y"),
              (7,"celcius/F")  
            )

def tagit(sender, instance, **kwargs):
    if type(instance) != Post:
        instance = Post.objects.get(id=instance.id)
    cache.set('categories', None)
    Tag.objects.update_tags(instance, instance.tags)


post_save.connect(tagit, sender=Post)
post_save.connect(tagit, sender=Recipe)
post_save.connect(tagit, sender=Ingredient)

from decimal import Decimal as D


class Unit(models.Model):
    metric = models.CharField(max_length=255)
    imperial = models.CharField(max_length=255)
    conversion = models.IntegerField(choices=CONVERSIONS)

    def __unicode__(self):
        return u"%s -> %s"% (self.metric, self.imperial)

    def to_imperial(self, amount):
        if self.conversion == 1L: # g -> oz
            return D('0.035') * amount
        if self.conversion == 2L: # k -> Lb
            return D('2.2') * amount
        if self.conversion == 3L: # ml -> foz
            return D('0.0338') * amount
        if self.conversion == 4L: # l -> foz
            return D('33.8') * amount
        if self.conversion == 5L: # cm -> inch
            return D('0.394') * amount
        if self.conversion == 6L: # m -> inch
            return D('39.4') * amount
        if self.conversion == 7L: # c -> F
            return D('1.8') * amount + 32
        if self.conversion == 8L: # ml -> cup
            return D('0.0042194092827004216') * amount
        if self.conversion == 9L: # l -> qt
            return D('0.0010570824524312897') * amount
        if self.conversion == 10L: # m -> y
            return D('1.0936133') * amount


from math import floor
from fractions import Fraction

def pretty(unit):

    int_part = int(floor(unit))
    if float(unit - int_part) <= 0.1:
        return str(int_part)
    r_part = str(Fraction.from_decimal(unit - int_part).limit_denominator(4))
    if r_part == '1':
        return str(int_part+1)

    if int_part == 0:
        return "%s"% ( r_part)

    return "%s + %s"% (int_part, r_part)

class Measurement(models.Model):
    recipe = models.ForeignKey(Recipe)
    ingredient = models.ForeignKey(Ingredient, null=True, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    unit = models.ForeignKey(Unit, null=True, blank=True)
    detail = models.CharField(max_length=255, null=True, blank=True)
    order = models.IntegerField()

    class Meta:
        ordering = ["order"]


    def metric(self):
        if self.unit:
            return " %s %s "% (pretty( self.amount ), self.unit.metric)
        else:
            return pretty( self.amount )
    
    def imperial(self):
        if (not self.unit):
            return ""

        return "( %s %s )"% (pretty( self.unit.to_imperial(self.amount) ), self.unit.imperial)


from django.contrib.comments.moderation import  moderator 
from comments_spamfighter.moderation import SpamFighterModerator
class PostModerator(SpamFighterModerator):
    # django's genric moderation options
    #auto_moderate_field = 'created'
    email_notification = True

    # comments spamfighter options
    akismet_check = True
    akismet_check_moderate = True
    keyword_check = True
    keyword_check_moderate = False


#PLEASE PLEASE don't kill me Niemeyer
if not (Post in moderator._registry) :
    moderator.register(Post, PostModerator)

