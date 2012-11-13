from django.utils.safestring import mark_safe
from django import template
from foodsite.core.models import Recipe
from django.template.loader import render_to_string
import re
register = template.Library()
from django.contrib.sites.models import Site
current_site = Site.objects.get_current()


@register.filter
def tagfy(tag, show_count=False):
    """
    tags are slugs but presented with space instead of underscores
    """
    count = 0
    tag_slug = tag.name
    tag_name = tag_slug.replace("_", " ")
    base = u'<a href="http://{domain}/tag/{tag}/" alt="{tag}" title="{tag}">{tag_name}'
    if show_count:
        base += u'({count})'
        count = tag.count
    base += u'</a>'
    return mark_safe(
        base.format(domain=current_site.domain, tag=tag_slug, tag_name=tag_name, count=count)
    )


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
        return mark_safe(render_to_string('partial/ingredients.html', {'measurements': recipe.measurement_set.all()}))
    except Recipe.DoesNotExist:
        return ""
#ingredients.mark_safe = True


sub_no_img = re.compile('![^! ]*!')


@register.filter
def no_img(texto):
    """
    strips textile imgs from text
    """
    return sub_no_img.sub("", texto)
