from django.conf.urls.defaults import patterns, include, url
import dgit.views
import os

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', dgit.views.index),
    url(r'^repo/(?P<repo_name>.*)/file/(?P<sha>.*)/$', dgit.views.file_),
    url(r'^repo/(?P<repo_name>.*)/tree/(?P<sha>.*)/$', dgit.views.tree),
    url(r'^repo/(?P<repo_name>.*)/filetree/(?P<sha>.*)/$', dgit.views.filetree),
    url(r'^repo/(?P<repo_name>.*)/commits/(?P<sha>.*)/$', dgit.views.commits),
    url(r'^repo/(?P<repo_name>.*)/commits/$', dgit.views.commits),
    url(r'^repo/(?P<repo_name>.*)/$', dgit.views.tree),

    
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^static/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': os.path.join(os.path.dirname(__file__), 'static_media')})
)
