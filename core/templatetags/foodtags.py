from django.template.defaultfilters import stringfilter,floatformat
from django.utils.safestring import mark_safe
from django import template
from foodsite.core.models import Recipe, Post
from django.template.loader import render_to_string
import re
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

@register.filter
def md5(valor=""):
    from hashlib import md5
    m = md5(str(valor).lower())
    return m.hexdigest()


@register.filter
def gravatinha(email):
    return mark_safe("<img src='http://www.gravatar.com/avatar/%s.jpg?s=80' />"% md5(email))


sub_sem_img = re.compile( '![^! ]*!')
@register.filter
def sem_img(texto):
    return sub_sem_img.sub("", texto)

