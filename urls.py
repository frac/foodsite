from django.conf.urls.defaults import *
from django.views.decorators.cache import cache_page

from foodsite.core.views import BlogFeed, AtomBlogFeed

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()
from foodsite.core.models import Post
from tagging.views import TaggedObjectList
from django.views.generic import ListView
from django.views.generic import DetailView

detail = {'queryset': Post.objects.all(), 'slug_field': 'slug'}
# detail_wave = {'queryset': Post.objects.all(), 'slug_field': 'slug', 'template_name': 'wave/post_detail_wave.html', 'mimetype': 'text/xml'}
# photo_wave = {'queryset': Photo.objects.all(), 'template_name': 'wave/photo_detail_wave.html', 'mimetype': 'text/xml'}

tag_queryset = Post.get_open()


feeds = {'rss': BlogFeed,
         'atom': AtomBlogFeed, }
from django.contrib.syndication.views import Feed

urlpatterns = patterns('',
    # Example:
    # (r'^secret_foodsite/', include('secret_foodsite.foo.urls')),

    (r'^$', cache_page(300)(ListView.as_view(queryset=tag_queryset))),
    (r'^post/(?P<slug>[-\w]+)$', cache_page(300)(DetailView.as_view(queryset=Post.objects.all(), slug_field='slug')), "post_detail"),
    (r'^testow/(?P<slug>[-\w]+)$', DetailView.as_view(queryset=Post.objects.all(), slug_field='slug'), "post_detail"),
    (r'^tag/(?P<tag>[-\w0-9\W]+)/$', cache_page(300)(TaggedObjectList.as_view(queryset_or_model=tag_queryset, extra_context={"menu": "tag"}, paginate_by=50))),
    # (r'^tag/(?P<tag>[-\w0-9\W]+)/$', tagged_object_list, {'queryset_or_model': tag_queryset, "extra_context": {"menu": "tag"}, 'paginate_by': 50}),
    (r'^feeds/(?P<url>.*)/$', Feed, {'feed_dict': feeds}),
    # (r'^comments/', include('django.contrib.comments.urls')),
    # (r'^wave/(?P<slug>[-\w]+)$', cache_page(300)(object_detail), detail_wave),
    # (r'^photowave/(?P<object_id>[0-9]+)$', cache_page(300)(object_detail), photo_wave),


    # (r'^detalhes$', direct_to_template, {'template': "detalhes.html"}),
    # Uncomment the admin/doc line below and add 'django.contrib.admindocs'
    # to INSTALLED_APPS to enable admin documentation:
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),
)

from django.conf import settings

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    )
