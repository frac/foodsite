from django.utils.safestring import mark_safe
from django import template
from foodsite.core.models import Recipe
from django.template.loader import render_to_string
import re
register = template.Library()


@register.filter
def ingredients(post):
    """
    if the post is a recipe post show ingredients
    It is necessary to do this way because of the inheritance of Post and Recipes
    """
    try:
        if type(post) == Recipe:
            recipe = post
        else:
            recipe = Recipe.objects.get(id=post.id)
        return mark_safe(render_to_string('partial/ingredients.html', { 'measurements': recipe.measurement_set.all() }))
    except Recipe.DoesNotExist:
        return ""
#ingredients.mark_safe = True


sub_no_img = re.compile( '![^! ]*!')
@register.filter
def no_img(texto):
    """
    strips textile imgs from text
    """
    return sub_no_img.sub("", texto)

