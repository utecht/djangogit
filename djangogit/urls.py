from django.conf.urls.defaults import patterns, include, url
import dgit.views
import os

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', dgit.views.index),
    url(r'^repo/(?P<repo_name>.*)/branch/(?P<ref>.*)/file/(?P<sha>.*)/$', dgit.views.file_),
    url(r'^repo/(?P<repo_name>.*)/branch/(?P<ref>.*)/commit/(?P<sha>.*)/$', dgit.views.commit),
    url(r'^repo/(?P<repo_name>.*)/branch/(?P<ref>.*)/tree/(?P<sha>.*)/$', dgit.views.tree),
    url(r'^repo/(?P<repo_name>.*)/branch/(?P<ref>.*)/$', dgit.views.repo),

    
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^static/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': os.path.join(os.path.dirname(__file__), 'static_media')})
)
