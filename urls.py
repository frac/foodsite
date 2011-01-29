from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template
from django.views.generic.list_detail import object_list, object_detail

from foodsite.core.views import list as post_list
from foodsite.core.views import BlogFeed, AtomBlogFeed

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()
import datetime
from foodsite.core.models import Post, Photo
from tagging.views import tagged_object_list


detail = {'queryset': Post.objects.all(), 'slug_field':'slug'}
detail_wave = {'queryset': Post.objects.all(), 'slug_field':'slug', 'template_name':'wave/post_detail_wave.html', 'mimetype':'text/xml'}
photo_wave = {'queryset': Photo.objects.all(),  'template_name':'wave/photo_detail_wave.html', 'mimetype':'text/xml'}

tag_queryset = Post.get_open()


feeds = {
        'rss': BlogFeed,
        'atom': AtomBlogFeed,
    }


urlpatterns = patterns('',
    # Example:
    # (r'^secret_foodsite/', include('secret_foodsite.foo.urls')),

    (r'^$', post_list),
    (r'^post/(?P<slug>[-\w]+)$',object_detail,detail, "post_detail"),
    (r'^tag/(?P<tag>[^/]+)/$',tagged_object_list, {'queryset_or_model':tag_queryset,"extra_context":{"menu":"tag"}, 'paginate_by':10}),
    (r'^feeds/(?P<url>.*)/$', 'django.contrib.syndication.views.feed', {'feed_dict': feeds}),
    (r'^comments/', include('django.contrib.comments.urls')),
    (r'^wave/(?P<slug>[-\w]+)$',object_detail,detail_wave),
    (r'^photowave/(?P<object_id>[0-9]+)$',object_detail,photo_wave),



    #(r'^detalhes$', direct_to_template, {'template': "detalhes.html"}),
    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),
)

from django.conf import settings

if settings.DEBUG:
    import os
    urlpatterns += patterns('',
        (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root' : settings.MEDIA_ROOT}),
        )

