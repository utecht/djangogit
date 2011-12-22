from django.conf.urls.defaults import patterns, include, url
import dgit.views


# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', dgit.views.index),
    url(r'^repo/(?P<repo_name>.*)/branch/(?P<ref>.*)/$', dgit.views.repo),
    url(r'^repo/(?P<repo_name>.*)/file/(?P<sha>.*)/$', dgit.views.file_),
    url(r'^repo/(?P<repo_name>.*)/commit/(?P<sha>.*)/$', dgit.views.commit),
    url(r'^repo/(?P<repo_name>.*)/tree/(?P<sha>.*)/$', dgit.views.tree),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
