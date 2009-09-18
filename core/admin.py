from django.contrib import admin
from django.contrib.auth.models import User
from models import *

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

class PostAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}
    list_display = ('title','pic','slug','published_at')
    ordering = ('-published_at',)

class IngredientAdmin(admin.ModelAdmin):
    list_display = ('title','pic',)
    ordering = ('pic',)



admin.site.register(Post, PostAdmin)
admin.site.register(Recipe,RecipeAdmin)
admin.site.register(Unit)
admin.site.register(Photo)
admin.site.register(Ingredient, IngredientAdmin)
