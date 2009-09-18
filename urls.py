from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template
from django.views.generic.list_detail import object_list, object_detail

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()
import datetime
from core.models import Post


detail = {'queryset': Post.objects.all(), 'slug_field':'slug'}

def list(request):
    posts =  Post.objects.filter(published_at__isnull=False,published_at__lte=datetime.datetime.today()).order_by('-published_at')
    page = request.GET.get("page",1) #pagination is 1 based
    return object_list(request, queryset=posts, page=page, paginate_by=20)


urlpatterns = patterns('',
    # Example:
    # (r'^secret_foodsite/', include('secret_foodsite.foo.urls')),

    (r'^$', list),
    (r'^post/(?P<slug>[-\w]+)$',object_detail,detail),
    (r'^detalhes$', direct_to_template, {'template': "detalhes.html"}),
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

