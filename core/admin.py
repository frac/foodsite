from django.contrib import admin
from django.contrib.auth.models import User
from models import *
import datetime

class PhotoInline(admin.TabularInline):
        model = Photo
        extra = 1


class MeasurementInline(admin.TabularInline):
        model = Measurement
        extra = 10

class RecipeAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}
    inlines = [MeasurementInline]
    list_display = ('title','pic','slug','published_at')
    ordering = ('-published_at',)

def publish(modeladmin, request, queryset):
    for obj in queryset:
        if not obj.published_at:
            obj.published_at=datetime.datetime.today()
            obj.save()


class PostAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}
    list_display = ('title','pic','slug','published_at')
    ordering = ('-published_at',)
    actions = [publish]

class IngredientAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}
    list_display = ('title','pic',)
    ordering = ('pic',)



class PhotoAdmin(admin.ModelAdmin):
    list_display = ('title','image','full_url')

class UnitAdmin(admin.ModelAdmin):
    list_display = ('metric','imperial','conversion')

admin.site.register(Post, PostAdmin)
admin.site.register(Recipe,RecipeAdmin)
admin.site.register(Unit, UnitAdmin)
admin.site.register(Photo, PhotoAdmin)
admin.site.register(Ingredient, IngredientAdmin)
