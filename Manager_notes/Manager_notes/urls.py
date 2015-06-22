from django.conf.urls import patterns, include, url
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^tinymce/', include('tinymce.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^auth/', include('Authenticated.urls')),
    url(r'^notes/', include('Notes.urls')),
    url(r'^', include('Authenticated.urls')),
)
