from django.conf.urls import url, include
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


urlpatterns = [
    # Example:
    # (r'^secret_foodsite/', include('secret_foodsite.foo.urls')),

    url(r'^$', cache_page(300)(ListView.as_view(queryset=tag_queryset))),
    url(r'^post/(?P<slug>[-\w]+)$', cache_page(300)(DetailView.as_view(queryset=Post.objects.all(), slug_field='slug')), name="post_detail"),
    url(r'^testow/(?P<slug>[-\w]+)$', DetailView.as_view(queryset=Post.objects.all(), slug_field='slug')),
    url(r'^tag/(?P<tag>[-\w0-9\W]+)/$', cache_page(300)(TaggedObjectList.as_view(queryset=tag_queryset, paginate_by=50))),  # extra_context={"menu": "tag"},
    # (r'^tag/(?P<tag>[-\w0-9\W]+)/$', tagged_object_list, {'queryset_or_model': tag_queryset, "extra_context": {"menu": "tag"}, 'paginate_by': 50}),
    url(r'^feeds/rss/$', BlogFeed()),
    url(r'^feeds/atom/$', AtomBlogFeed()),
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
]

from django.conf import settings

#if settings.DEBUG:
#    urlpatterns += patterns('',
#        url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
#    )
