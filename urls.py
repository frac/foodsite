from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template
from django.views.generic.list_detail import object_list, object_detail

from core.views import list as post_list
from core.views import BlogFeed, AtomBlogFeed

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()
import datetime
from core.models import Post
from tagging.views import tagged_object_list


detail = {'queryset': Post.objects.all(), 'slug_field':'slug'}

tag_queryset = Post.get_open()


feeds = {
        'rss': BlogFeed,
        'atom': AtomBlogFeed,
    }


urlpatterns = patterns('',
    # Example:
    # (r'^secret_foodsite/', include('secret_foodsite.foo.urls')),

    (r'^$', post_list),
    (r'^post/(?P<slug>[-\w]+)$',object_detail,detail),
    (r'^tag/(?P<tag>[^/]+)/$',tagged_object_list, {'queryset_or_model':tag_queryset,"extra_context":{"menu":"tag"}}),
    (r'^feeds/(?P<url>.*)/$', 'django.contrib.syndication.views.feed', {'feed_dict': feeds}),
    (r'^comments/', include('django.contrib.comments.urls')),



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

