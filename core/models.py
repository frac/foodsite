import datetime
import os
import Image
import ImageOps
from decimal import Decimal as D

from django.db import models
from django.db.models.signals import post_save, pre_delete
from django.core.cache import cache

from tagging.fields import TagField
from tagging.models import Tag

from util import prettyprint
from foodsite.settings import SITE_URL, MEDIA_URL

MAX_SIZE = 970
SMALL_SIZE = 450
THUMB_SIZE = 210


class Photo(models.Model):
    """
    store user generated pictures
    """
    title = models.CharField(max_length=255)
    image = models.ImageField(upload_to='photos/%Y/%m/%d')
    author = models.CharField(max_length=255, default="Adriano Petrich")
    used = models.BooleanField(default=False)

    class Meta:
        ordering = ["-image"]

    def __unicode__(self):
        return u"%s" % (self.title)

    @property
    def thumb(self):
        path = str(self.image)
        return "%s_t%s" % (path[:-4], path[-4:])

    @property
    def small(self):
        path = str(self.image)
        return "%s_s%s" % (path[:-4], path[-4:])

    @property
    def full_url(self):
        path = str(self.image)
        return "%s%s_s%s" % (MEDIA_URL, path[:-4], path[-4:])

    def wave(self):
        path = str(self.image)
        return "<img src='%s%s_t%s'/>" % (MEDIA_URL, path[:-4], path[-4:])
    wave.allow_tags = True
    wave.short_description = 'Imagem'

    def thumb_exists(self):
        os.path.isfile(self.get_path(thumb=True))

    def get_path(self, thumb=False):
        if thumb:
            return "%s_t%s" % (self.image.path[:-4], self.image.path[-4:])
        else:
            return "%s_s%s" % (self.image.path[:-4], self.image.path[-4:])

    def create_thumb(self):
        """
        Reformat and create small and thumbnail images.
        All pictures are squared for artistic reasons :)
        """
        self.image.seek(0)
        original = Image.open(self.image)
        if original.mode not in ('L', 'RGB'):
            original = original.convert('RGB')

        quality_val = 95
        dpi_val = (150, 150)

        format = original.format
        min_dim = min(original.size)
        #original = original.crop((0,0,min_dim,min_dim))

        #make it square
        original = ImageOps.fit(original, (min_dim, min_dim), centering=(0.5, 0.5))

        #make large
        im = original.resize((MAX_SIZE, MAX_SIZE), Image.ANTIALIAS)
        im.save(self.image.path, format, quality=quality_val, dpi=dpi_val)

        #make small
        im = original.resize((SMALL_SIZE, SMALL_SIZE), Image.ANTIALIAS)
        im.save(self.get_path(thumb=False), format, quality=quality_val, dpi=dpi_val)

        # Make Thumb
        im = original.resize((THUMB_SIZE, THUMB_SIZE), Image.ANTIALIAS)
        im.save(self.get_path(thumb=True), format, quality=quality_val, dpi=dpi_val)

    def destroy_thumb(self):
        """
        Delete all files when we delete the model
        Files might not exist, see if I care.
        """
        try:
            os.unlink(self.get_path(thumb=True))
        except OSError:
            pass
        try:
            os.unlink(self.get_path(thumb=False))
        except OSError:
            pass
        try:
            os.unlink(self.image.path)
        except OSError:
            pass


def cria_visualizacao(sender, **kwargs):
    instance = kwargs["instance"]
    if instance.image:
        if not instance.thumb_exists():
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
    author = models.CharField(max_length=255, default="Adriano Petrich")

    @property
    def enable_comments(self):
        return True

    @property
    def full_url(self):
        return "%spost/%s" % (SITE_URL, self.slug)

    class Meta:
        ordering = ["-published_at"]

    def set_tags(self, tags):
        Tag.objects.update_tags(self, tags)

    def get_tags(self):
        return Tag.objects.get_for_object(self)

    def __unicode__(self):
        return u"%s" % self.slug

    def get_next(self):
        try:
            self._next
        except AttributeError:
            self._next = None
        try:
            if self._next is None:
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

            if self._previous is None:
                self._previous = Post.get_open().filter(published_at__lt=self.published_at).order_by("-published_at")[0]
            return self._previous
        except:
            return None

    @property
    def wave(self):
        return "%swave/%s" % (SITE_URL, self.slug)

    @models.permalink
    def get_absolute_url(self):
        """
        This is the more correct way of geting the url for the resource.
        """
        return ("post_detail", "", {"slug": self.slug})

    @staticmethod
    def get_open():
        """
        Queryset with the published posts
        """
        return Post.objects.filter(published_at__isnull=False, published_at__lte=datetime.datetime.today()).order_by('-published_at')


class Recipe(Post):
    """
    Recipe differs with posts only that they have Measurements associated with them.
    """
    pass


class Ingredient(Post):
    @property
    def name(self):
        return self.title

    class Meta:
        ordering = ["title"]


CONVERSIONS = ((0, "No conversion"),
              (1, "g/oz"),
              (2, "k/Lb"),
              (3, "ml/foz"),
              (8, "ml/cup"),
              (4, "l/foz"),
              (9, "l/quart"),
              (5, "cm/inch"),
              (6, "m/inch"),
              (10, "m/y"),
              (7, "celcius/F"))


def tagit(sender, instance, **kwargs):
    if type(instance) != Post:
        instance = Post.objects.get(id=instance.id)
    cache.set('categories', None)
    Tag.objects.update_tags(instance, instance.tags)


post_save.connect(tagit, sender=Post)
post_save.connect(tagit, sender=Recipe)
post_save.connect(tagit, sender=Ingredient)


class Unit(models.Model):
    """
    This could be a dictionary, but in the end It payed up to have it as a model.
    Sometimes I want to add a unit like "leaves" or "cloves" that do not need conversion,
    but looks nicer in the blog.
    """
    metric = models.CharField(max_length=255)
    imperial = models.CharField(max_length=255)
    conversion = models.IntegerField(choices=CONVERSIONS)

    def __unicode__(self):
        return u"%s -> %s" % (self.metric, self.imperial)

    def to_imperial(self, amount):
        if self.conversion == 1L:  # g -> oz
            return D('0.035') * amount
        if self.conversion == 2L:  # k -> Lb
            return D('2.2') * amount
        if self.conversion == 3L:  # ml -> foz
            return D('0.0338') * amount
        if self.conversion == 4L:  # l -> foz
            return D('33.8') * amount
        if self.conversion == 5L:  # cm -> inch
            return D('0.394') * amount
        if self.conversion == 6L:  # m -> inch
            return D('39.4') * amount
        if self.conversion == 7L:  # c -> F
            return D('1.8') * amount + 32
        if self.conversion == 8L:  # ml -> cup
            return D('0.0042194092827004216') * amount
        if self.conversion == 9L:  # l -> qt
            return D('0.0010570824524312897') * amount
        if self.conversion == 10L:  # m -> y
            return D('1.0936133') * amount


class Measurement(models.Model):
    """
    binds a recipe to ingredients.
    """
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
            return " %s %s " % (prettyprint(self.amount), self.unit.metric)
        else:
            return prettyprint(self.amount)

    def imperial(self):
        if (not self.unit) or (self.unit.conversion == 0L):
            return ""

        return "( %s %s )" % (prettyprint(self.unit.to_imperial(self.amount)), self.unit.imperial)
