from django.template.defaultfilters import stringfilter,floatformat
from django.utils.safestring import mark_safe
from django import template
from foodsite.core.models import Recipe, Post
from django.template.loader import render_to_string

register = template.Library()


@register.filter
def ingredients(post):
    try:
        if type(post) == Recipe:
            receita = post
        else:
            receita = Recipe.objects.get(id=post.id)
        return mark_safe(render_to_string('partial/ingredients.html', { 'measurements': receita.measurement_set.all() }))
    except Recipe.DoesNotExist:
        return ""
#ingredients.mark_safe = True

