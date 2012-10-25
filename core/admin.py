from django.db.models import Q
from django.contrib import admin
from models import Measurement, Post, Photo
from models import Recipe, Ingredient, Unit
import datetime
from django_push.publisher import ping_hub


class MeasurementInline(admin.TabularInline):
    model = Measurement
    extra = 10


def publish(modeladmin, request, queryset):
    for obj in queryset:
        if not obj.published_at:
            obj.published_at = datetime.datetime.today()
            obj.save()
    ping_hub('http://sfp.adrianopetrich.com/feeds/atom/')


def use_photo(modeladmin, request, queryset):
    for obj in queryset:
        if not obj.used:
            obj.used = True
            obj.save()


class PostAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}
    list_display = ('title', 'pic', 'slug', 'published_at')
    ordering = ('-published_at',)
    actions = [publish]
    change_form_template = "admin/change_view_form.html"

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        """
        Show only pictures that have not been used or that belongs to posts
        """
        if db_field.name == "pic":
            kwargs["queryset"] = Photo.objects.filter(Q(used=False) | Q(post__isnull=False)).distinct()
            return db_field.formfield(**kwargs)
        return super(PostAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)


class RecipeAdmin(PostAdmin):
    inlines = [MeasurementInline]
    list_display = ('title', 'wave', 'pic', 'slug', 'tags', 'published_at')

    # have to apear again because of the return super
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        """
        Show only pictures that have not been used or that belongs to posts
        """
        if db_field.name == "pic":
            kwargs["queryset"] = Photo.objects.filter(Q(used=False) | Q(post__isnull=False)).distinct()
            return db_field.formfield(**kwargs)
        return super(RecipeAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)


class IngredientAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}
    list_display = ('title', 'pic',)
    ordering = ('pic',)
    change_form_template = "admin/change_view_form.html"


class PhotoAdmin(admin.ModelAdmin):
    list_display = ('title', 'used', 'full_url', 'wave')
    list_filter = ('used',)
    actions = [use_photo]


class UnitAdmin(admin.ModelAdmin):
    list_display = ('metric', 'imperial', 'conversion')

admin.site.register(Post, PostAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Unit, UnitAdmin)
admin.site.register(Photo, PhotoAdmin)
admin.site.register(Ingredient, IngredientAdmin)
